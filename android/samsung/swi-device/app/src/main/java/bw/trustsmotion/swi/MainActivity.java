package bw.trustsmotion.swi;

import android.Manifest;
import android.app.Activity;
import android.os.Build;
import android.os.Bundle;
import android.content.pm.PackageManager;
import android.graphics.Color;
import android.view.Gravity;
import android.widget.LinearLayout;
import android.widget.TextView;

public class MainActivity extends Activity {
    private int dp(float value) {
        return (int)(value * getResources().getDisplayMetrics().density);
    }

    @Override
    protected void onCreate(Bundle state) {
        super.onCreate(state);

        if (Build.VERSION.SDK_INT >= 33 &&
            checkSelfPermission(Manifest.permission.POST_NOTIFICATIONS)
                != PackageManager.PERMISSION_GRANTED) {
            requestPermissions(
                new String[]{Manifest.permission.POST_NOTIFICATIONS}, 100
            );
        }

        LinearLayout page = new LinearLayout(this);
        page.setOrientation(LinearLayout.VERTICAL);
        page.setGravity(Gravity.CENTER_HORIZONTAL);
        page.setPadding(dp(24), dp(48), dp(24), dp(24));
        page.setBackgroundColor(Color.rgb(15, 17, 20));

        TextView logo = new TextView(this);
        logo.setText("SWI");
        logo.setTextSize(48);
        logo.setTextColor(Color.rgb(229, 138, 38));
        logo.setGravity(Gravity.CENTER);

        TextView name = new TextView(this);
        name.setText("STRUCTURED WORKFLOW INTELLIGENCE");
        name.setTextSize(14);
        name.setTextColor(Color.WHITE);
        name.setGravity(Gravity.CENTER);

        TextView identity = new TextView(this);
        identity.setText("\nTHIS DEVICE HAS SWI\n");
        identity.setTextSize(20);
        identity.setTextColor(Color.WHITE);
        identity.setGravity(Gravity.CENTER);

        TextView status = new TextView(this);
        status.setText(
            "SWI APPLICATION: RUNNING\n" +
            "DEVICE IDENTITY: NOT YET ATTESTED\n" +
            "GOVERNING SPINE: NOT CONNECTED\n" +
            "PRODUCTION AUTHORIZATION: NO"
        );
        status.setTextSize(15);
        status.setTextColor(Color.rgb(190, 200, 210));
        status.setGravity(Gravity.CENTER);
        status.setPadding(0, dp(24), 0, dp(24));

        TextView footer = new TextView(this);
        footer.setText("Trust is evidence that can be examined.");
        footer.setTextColor(Color.rgb(229, 138, 38));
        footer.setGravity(Gravity.CENTER);

        page.addView(logo);
        page.addView(name);
        page.addView(identity);
        page.addView(status);
        page.addView(footer);

        setContentView(page);
    }
}
