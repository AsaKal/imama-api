package com.yourpackage.app;

import android.content.Intent;
import android.os.Bundle;
import android.view.LayoutInflater;
import android.view.View;
import android.widget.ImageButton;
import android.widget.ImageView;
import android.widget.PopupWindow;
import android.widget.Switch;
import android.widget.Toast;

import androidx.appcompat.app.AppCompatActivity;

public class LandingActivity extends AppCompatActivity {

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        // Must run before super.onCreate() so the saved theme applies
        // before the layout inflates.
        ThemeManager.applySavedTheme(this);
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_landing);

        ImageView ivAvatar = findViewById(R.id.ivAvatar);
        ImageButton btnMenu = findViewById(R.id.btnMenu);

        // Tapping the avatar opens the chat screen
        ivAvatar.setOnClickListener(v -> {
            Intent intent = new Intent(LandingActivity.this, ChatActivity.class);
            startActivity(intent);
        });

        // Tapping the hamburger icon opens the dropdown menu
        btnMenu.setOnClickListener(this::showMainMenuPopup);

        // "Makala" tab — wire this to your articles list screen once you add it
        findViewById(R.id.tabMakala).setOnClickListener(v ->
                Toast.makeText(this, "TODO: open Makala (articles) screen", Toast.LENGTH_SHORT).show()
        );

        // "Sasisha" — wire this to your pregnancy-update flow
        findViewById(R.id.btnSasisha).setOnClickListener(v ->
                Toast.makeText(this, "TODO: open update-pregnancy flow", Toast.LENGTH_SHORT).show()
        );

        // "Soma" — wire this to your article detail screen
        findViewById(R.id.btnSoma).setOnClickListener(v ->
                Toast.makeText(this, "TODO: open article detail screen", Toast.LENGTH_SHORT).show()
        );
    }

    private void showMainMenuPopup(View anchor) {
        View popupView = LayoutInflater.from(this).inflate(R.layout.popup_main_menu, null);

        PopupWindow popupWindow = new PopupWindow(
                popupView,
                View.MeasureSpec.UNSPECIFIED,
                View.MeasureSpec.UNSPECIFIED,
                true
        );
        popupWindow.setElevation(12f);

        // Dark mode switch — reflects saved state and persists changes immediately
        Switch switchDarkMode = popupView.findViewById(R.id.switchDarkMode);
        switchDarkMode.setChecked(ThemeManager.isDarkModeEnabled(this));
        switchDarkMode.setOnCheckedChangeListener((buttonView, isChecked) -> {
            ThemeManager.setDarkModeEnabled(this, isChecked);
            popupWindow.dismiss();
            recreate(); // reload this Activity so the new theme colors apply immediately
        });

        popupView.findViewById(R.id.menuEditPregnancy).setOnClickListener(v -> {
            popupWindow.dismiss();
            Toast.makeText(this, "TODO: open Hariri Ujauzito screen", Toast.LENGTH_SHORT).show();
        });

        popupView.findViewById(R.id.menuEditAge).setOnClickListener(v -> {
            popupWindow.dismiss();
            Toast.makeText(this, "TODO: open Hariri Umri screen", Toast.LENGTH_SHORT).show();
        });

        popupView.findViewById(R.id.menuEditWeight).setOnClickListener(v -> {
            popupWindow.dismiss();
            Toast.makeText(this, "TODO: open Hariri Uzito screen", Toast.LENGTH_SHORT).show();
        });

        popupView.findViewById(R.id.menuShare).setOnClickListener(v -> {
            popupWindow.dismiss();
            Intent shareIntent = new Intent(Intent.ACTION_SEND);
            shareIntent.setType("text/plain");
            shareIntent.putExtra(Intent.EXTRA_TEXT, "Nakushirikisha programu hii!");
            startActivity(Intent.createChooser(shareIntent, "Shirikisha kupitia"));
        });

        popupView.findViewById(R.id.menuLogout).setOnClickListener(v -> {
            popupWindow.dismiss();
            Toast.makeText(this, "TODO: sign the user out", Toast.LENGTH_SHORT).show();
        });

        popupView.findViewById(R.id.menuTerms).setOnClickListener(v -> {
            popupWindow.dismiss();
            Toast.makeText(this, "TODO: open Sheria na Masharti screen", Toast.LENGTH_SHORT).show();
        });

        popupView.findViewById(R.id.menuPrivacy).setOnClickListener(v -> {
            popupWindow.dismiss();
            Toast.makeText(this, "TODO: open Sera ya Faragha screen", Toast.LENGTH_SHORT).show();
        });

        popupView.findViewById(R.id.menuContact).setOnClickListener(v -> {
            popupWindow.dismiss();
            Toast.makeText(this, "TODO: open Wasiliana Nasi screen", Toast.LENGTH_SHORT).show();
        });

        popupWindow.showAsDropDown(anchor, -240, 12);
    }
}
