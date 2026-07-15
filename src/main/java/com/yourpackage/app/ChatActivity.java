package com.yourpackage.app;

import android.os.Bundle;
import android.text.format.DateFormat;
import android.view.LayoutInflater;
import android.view.View;
import android.widget.EditText;
import android.widget.ImageButton;
import android.widget.PopupWindow;
import android.widget.Toast;

import androidx.appcompat.app.AppCompatActivity;
import androidx.recyclerview.widget.LinearLayoutManager;
import androidx.recyclerview.widget.RecyclerView;

import java.util.ArrayList;
import java.util.Calendar;
import java.util.List;

public class ChatActivity extends AppCompatActivity {

    private List<Message> messages;
    private MessageAdapter adapter;
    private RecyclerView rvMessages;
    private EditText etInput;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        ThemeManager.applySavedTheme(this);
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_chat);

        rvMessages = findViewById(R.id.rvMessages);
        etInput = findViewById(R.id.etInput);
        ImageButton btnSend = findViewById(R.id.btnSend);
        ImageButton btnBack = findViewById(R.id.btnBack);
        ImageButton btnMoreOptions = findViewById(R.id.btnMoreOptions);

        messages = new ArrayList<>();
        messages.add(new Message("Hey! I'm your assistant. Ask me anything.", currentTime(), Message.TYPE_BOT));

        adapter = new MessageAdapter(messages);
        rvMessages.setLayoutManager(new LinearLayoutManager(this));
        rvMessages.setAdapter(adapter);

        btnSend.setOnClickListener(v -> sendMessage());
        btnBack.setOnClickListener(v -> finish());
        btnMoreOptions.setOnClickListener(this::showChatOptionsPopup);
    }

    /**
     * Shows the "add photo" / "voice input" popup, anchored above the
     * more-options button to the left of the chat input.
     */
    private void showChatOptionsPopup(View anchor) {
        View popupView = LayoutInflater.from(this).inflate(R.layout.popup_chat_options, null);

        PopupWindow popupWindow = new PopupWindow(
                popupView,
                View.MeasureSpec.UNSPECIFIED,
                View.MeasureSpec.UNSPECIFIED,
                true
        );
        popupWindow.setElevation(8f);

        View optionAddPhoto = popupView.findViewById(R.id.optionAddPhoto);
        View optionVoiceInput = popupView.findViewById(R.id.optionVoiceInput);

        optionAddPhoto.setOnClickListener(v -> {
            popupWindow.dismiss();
            openImagePicker();
        });

        optionVoiceInput.setOnClickListener(v -> {
            popupWindow.dismiss();
            startVoiceInput();
        });

        // Show above the anchor button since it sits at the bottom of the screen
        popupWindow.showAsDropDown(anchor, 0, -(anchor.getHeight() + popupView.getMeasuredHeight() + 220));
    }

    /**
     * TODO: Replace with a real image picker (ActivityResultContracts.PickVisualMedia
     * or an Intent.ACTION_PICK on MediaStore.Images.Media.EXTERNAL_CONTENT_URI),
     * plus READ_MEDIA_IMAGES / READ_EXTERNAL_STORAGE permission handling on
     * older API levels.
     */
    private void openImagePicker() {
        Toast.makeText(this, "TODO: open gallery / image picker", Toast.LENGTH_SHORT).show();
    }

    /**
     * TODO: Replace with android.speech.RecognizerIntent
     * (RecognizerIntent.ACTION_RECOGNIZE_SPEECH) plus RECORD_AUDIO permission
     * handling, then feed the recognized text into etInput.
     */
    private void startVoiceInput() {
        Toast.makeText(this, "TODO: start voice input", Toast.LENGTH_SHORT).show();
    }

    private void sendMessage() {
        String text = etInput.getText().toString().trim();
        if (text.isEmpty()) return;

        messages.add(new Message(text, currentTime(), Message.TYPE_USER));
        adapter.notifyItemInserted(messages.size() - 1);
        rvMessages.scrollToPosition(messages.size() - 1);
        etInput.setText("");

        // Placeholder bot reply — replace this block with your FastAPI network call
        rvMessages.postDelayed(() -> {
            messages.add(new Message("Got it — let me look into that.", currentTime(), Message.TYPE_BOT));
            adapter.notifyItemInserted(messages.size() - 1);
            rvMessages.scrollToPosition(messages.size() - 1);
        }, 1200);
    }

    private String currentTime() {
        return DateFormat.format("HH:mm", Calendar.getInstance()).toString();
    }
}
