package bw.trustsmotion.swi;

import android.app.PendingIntent;
import android.appwidget.AppWidgetManager;
import android.appwidget.AppWidgetProvider;
import android.content.Context;
import android.content.Intent;
import android.widget.RemoteViews;

public class SWIWidgetProvider extends AppWidgetProvider {
    @Override
    public void onUpdate(Context context, AppWidgetManager manager,
                         int[] ids) {
        for (int id : ids) {
            RemoteViews views = new RemoteViews(
                context.getPackageName(), R.layout.swi_widget
            );

            Intent open = new Intent(context, MainActivity.class);
            PendingIntent pending = PendingIntent.getActivity(
                context, 0, open,
                PendingIntent.FLAG_UPDATE_CURRENT |
                PendingIntent.FLAG_IMMUTABLE
            );

            views.setOnClickPendingIntent(R.id.swi_widget_root, pending);
            manager.updateAppWidget(id, views);
        }
    }
}
