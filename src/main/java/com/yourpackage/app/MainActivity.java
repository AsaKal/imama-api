package com.yourpackage.app;

import android.os.Bundle;
import android.text.format.DateFormat;
import android.widget.EditText;
import android.widget.ImageButton;

import androidx.appcompat.app.AppCompatActivity;
import androidx.recyclerview.widget.LinearLayoutManager;
import androidx.recyclerview.widget.RecyclerView;

import java.util.ArrayList;
import java.util.Calendar;
import java.util.List;

public class MainActivity extends AppCompatActivity {

    private List<Message> messages;
    private MessageAdapter adapter;
    private RecyclerView rvMessages;
    private EditText etInput;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);

        rvMessages = findViewById(R.id.rvMessages);
        etInput = findViewById(R.id.etInput);
        ImageButton btnSend = findViewById(R.id.btnSend);

        messages = new ArrayList<>();
        messages.add(new Message("Hey! I'm your assistant. Ask me anything.", currentTime(), Message.TYPE_BOT));

        adapter = new MessageAdapter(messages);
        rvMessages.setLayoutManager(new LinearLayoutManager(this));
        rvMessages.setAdapter(adapter);

        btnSend.setOnClickListener(v -> sendMessage());
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
