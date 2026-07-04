import os
import re
import time
import uuid
import logging

os.environ.setdefault("PYTORCH_CUDA_ALLOC_CONF", "expandable_segments:True")

logger = logging.getLogger(__name__)

MODEL_DIR = "/home/eth22/Desktop/imama/imama-api/models"
CONVERSATION_TTL = 24 * 60 * 60  # 24 hours

SYSTEM_PROMPT = """Your name is Imama, you are a polite and proffessional swahili speaking medical bot with extensive proffessional knowledge on the
following diseases:,
UTI
Pre eclampsia.
You are owned by Aspire Analytics Co LTD.

In a compassionate manner you help pregnant women to identify what they might be suffering from by asking them a
series of swahili questions like:
Duration of pregnancy time
Pressure levels (if they know)
Fever,

Maximum pregnancy duration time is 42 weeks or 9 months. If user provides outside this timeframe, ask them to correct themselves!

If duration of pregnancy time is less than 20 weeks then ask a series of questions in multiple steps relating to UTI!,
but dont hint the likelihood of UTI until you satisfy yourself with the information. Questions like the following have to be asked:
Pain when urinating
Urine color
and others relating to UTI.

If duration of pregnancy time is greater than 20 weeks then ask a series of questions in multiple steps relating to Pre Eclampsia!,
but dont hint the likelihood of Pre eclampsia until you satisfy yourself with the information. Questions like these have to be asked:
difficulty in breathing,
fainting
and any related to pre eclampsia

At any point you might mix question in order to come up with a precise diagnosis.
Dont rush to conclude, take your time in a proffessional manner to diagnose the woman!.
Use the information to predict whether a pregnant woman is likely suffering from either UTI or Pre eclampsia and not both.

Give out recommendations only when you have extensively collected all necessary symptoms for the detection of either
UTI or Pre eclampsia.

If no symptoms match either UTI or Pre eclampsia:
Be sympathetic
tell the woman you don't have knowledge on the disease she might be suffering
Strongly recommend her for further medical checkup.
Strictly keep the conversation in simple and fluent swahili language.

Occasionally, you can suggest to user gynecologists contacts who are in Tanzania within Dar es Salaam city only if they agree,
be specific on this! Fetch their contacts from knowledge base and not online! Only suggest these once, and dont do it again for th same user.
"""

# Gemma4's chat format wraps internal reasoning in a "thought" channel and
# terminates each turn with <turn|>; only the trailing content is the reply
# meant for the user (see models/tokenizer_config.json's response_schema).
RESPONSE_PATTERN = re.compile(
    r"(<\|channel>thought\n(?P<thinking>.*?)<channel\|>)?"
    r"(?P<tool_calls><\|tool_call>.*<tool_call\|>)?"
    r"(?P<content>(?:(?!<turn\|>)(?!<\|tool_response>).)+)?"
    r"(?:<turn\|>|<\|tool_response>)?",
    re.DOTALL,
)


class ChatService:
    def __init__(self):
        self.processor = None
        self.model = None
        self.model_loaded = False
        self.conversations: dict[str, dict] = {}

    def load_model(self):
        """Load HuggingFace model and processor from the local models directory."""
        try:
            from transformers import AutoProcessor, AutoModelForCausalLM
            import torch

            logger.info("Loading processor from %s", MODEL_DIR)
            self.processor = AutoProcessor.from_pretrained(
                str(MODEL_DIR), trust_remote_code=True
            )

            logger.info("Loading model weights from %s", MODEL_DIR)
            self.model = AutoModelForCausalLM.from_pretrained(
                str(MODEL_DIR),
                trust_remote_code=True,
                dtype=torch.bfloat16,
                device_map="auto",
                max_memory={0: "5GiB", "cpu": "28GiB"},
            )
            self.model.eval()
            self.model_loaded = True
            logger.info("Model loaded successfully")

        except Exception as e:
            logger.error("Model failed to load: %s", e)
            logger.warning("Chat service will run without a loaded model")

    def unload_model(self):
        """Release model weights and free memory on shutdown."""
        if not self.model_loaded:
            return
        import gc
        import torch
        self.model = None
        self.processor = None
        self.model_loaded = False
        torch.cuda.empty_cache()
        gc.collect()
        logger.info("Model unloaded.")

    # ------------------------------------------------------------------ #
    # Session management
    # ------------------------------------------------------------------ #

    def _cleanup_expired(self):
        now = time.time()
        expired = [
            cid
            for cid, data in self.conversations.items()
            if now - data["last_active"] > CONVERSATION_TTL
        ]
        for cid in expired:
            del self.conversations[cid]

    def create_conversation(self, user_id: str) -> str:
        self._cleanup_expired()
        conversation_id = str(uuid.uuid4())
        self.conversations[conversation_id] = {
            "user_id": user_id,
            "history": [],           # list of {"role": str, "content": str}
            "last_active": time.time(),
            "contacts_sent": False,
        }
        return conversation_id

    def delete_conversation(self, conversation_id: str) -> bool:
        if conversation_id in self.conversations:
            del self.conversations[conversation_id]
            return True
        return False

    def get_conversation(self, conversation_id: str) -> dict | None:
        return self.conversations.get(conversation_id)

    # ------------------------------------------------------------------ #
    # Inference
    # ------------------------------------------------------------------ #

    def _build_messages(self, conversation: dict, user_message: str) -> list[dict]:
        messages = [{"role": "system", "content": SYSTEM_PROMPT}]
        messages.extend(conversation["history"])
        messages.append({"role": "user", "content": user_message})
        return messages

    def _generate_pytorch(self, messages: list[dict]) -> str:
        import torch

        text = self.processor.apply_chat_template(
            messages,
            tokenize=False,
            add_generation_prompt=True,
        )
        inputs = self.processor(text=text, return_tensors="pt").to(self.model.device)

        with torch.no_grad():
            output_ids = self.model.generate(
                **inputs,
                max_new_tokens=512,
                do_sample=True,
                temperature=0.7,
                top_p=0.9,
                repetition_penalty=1.1,
                pad_token_id=self.processor.tokenizer.pad_token_id,
                eos_token_id=self.model.generation_config.eos_token_id,
            )

        # Decode only newly generated tokens, keeping special tokens so the
        # thought-channel markers can be stripped by the response pattern.
        generated = output_ids[0][inputs["input_ids"].shape[-1]:]
        raw_text = self.processor.decode(generated, skip_special_tokens=False)

        match = RESPONSE_PATTERN.match(raw_text)
        content = match.group("content") if match else None
        return (content or raw_text).strip()

    def generate_response(
        self, conversation_id: str, user_id: str, user_message: str
    ) -> str:
        """
        Generate a response for the given conversation and user message.
        Raises PermissionError if the conversation belongs to another user,
        or RuntimeError if the model is not loaded.
        """
        self._cleanup_expired()

        if conversation_id not in self.conversations:
            self.conversations[conversation_id] = {
                "user_id": user_id,
                "history": [],
                "last_active": time.time(),
                "contacts_sent": False,
            }

        conversation = self.conversations[conversation_id]
        if conversation["user_id"] != user_id:
            raise PermissionError("Conversation does not belong to this user.")
        conversation["last_active"] = time.time()

        if not self.model_loaded:
            raise RuntimeError(
                "Model is not loaded. Ensure model weights are present in app/models/."
            )

        messages = self._build_messages(conversation, user_message)
        response = self._generate_pytorch(messages)

        conversation["history"].append({"role": "user", "content": user_message})
        conversation["history"].append({"role": "assistant", "content": response})

        return response


# Singleton instance shared across the app
chat_service = ChatService()
