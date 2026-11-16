package bw.trustsmotion.swi;

import android.content.Intent;
import android.service.quicksettings.Tile;
import android.service.quicksettings.TileService;

public class SWIQuickTileService extends TileService {
    @Override
    public void onStartListening() {
        super.onStartListening();
        Tile tile = getQsTile();
        if (tile != null) {
            tile.setLabel("SWI");
            if (android.os.Build.VERSION.SDK_INT >= 29) {
                tile.setSubtitle("Open SWI Device");
            }
            tile.setState(Tile.STATE_INACTIVE);
            tile.updateTile();
        }
    }

    @Override
    public void onClick() {
        super.onClick();
        Intent intent = new Intent(this, MainActivity.class);
        intent.addFlags(Intent.FLAG_ACTIVITY_NEW_TASK);
        startActivityAndCollapse(intent);
    }
}
