package bw.trustsmotion.swi;

import android.Manifest;
import android.app.Notification;
import android.app.NotificationChannel;
import android.app.NotificationManager;
import android.app.PendingIntent;
import android.content.BroadcastReceiver;
import android.content.Context;
import android.content.Intent;
import android.content.pm.PackageManager;
import android.os.Build;

public class SWIBootReceiver extends BroadcastReceiver {
    @Override
    public void onReceive(Context context, Intent intent) {
        if (!Intent.ACTION_BOOT_COMPLETED.equals(intent.getAction())) return;

        if (Build.VERSION.SDK_INT >= 33 &&
            context.checkSelfPermission(Manifest.permission.POST_NOTIFICATIONS)
                != PackageManager.PERMISSION_GRANTED) return;

        NotificationManager manager =
            (NotificationManager) context.getSystemService(
                Context.NOTIFICATION_SERVICE
            );

        String channel = "swi_device_startup";
        if (Build.VERSION.SDK_INT >= 26) {
            manager.createNotificationChannel(new NotificationChannel(
                channel, "SWI Device Startup",
                NotificationManager.IMPORTANCE_DEFAULT
            ));
        }

        Intent open = new Intent(context, MainActivity.class);
        PendingIntent pending = PendingIntent.getActivity(
            context, 0, open,
            PendingIntent.FLAG_UPDATE_CURRENT | PendingIntent.FLAG_IMMUTABLE
        );

        Notification.Builder builder =
            Build.VERSION.SDK_INT >= 26
                ? new Notification.Builder(context, channel)
                : new Notification.Builder(context);

        builder.setSmallIcon(android.R.drawable.ic_dialog_info)
            .setContentTitle("SWI is available")
            .setContentText("Open SWI Device status")
            .setContentIntent(pending)
            .setAutoCancel(true);

        manager.notify(1001, builder.build());
    }
}
