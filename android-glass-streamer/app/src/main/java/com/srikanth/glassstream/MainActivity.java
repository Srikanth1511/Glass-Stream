package com.srikanth.glassstream;

import android.app.Activity;
import android.content.Intent;
import android.os.Bundle;
import android.view.View;
import android.widget.Button;
import android.widget.TextView;

import com.srikanth.glassstream.svc.StreamService;

public class MainActivity extends Activity {
    private TextView info;
    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);
        info  = (TextView) findViewById(R.id.info);
        Button start = (Button) findViewById(R.id.btnStart);
        Button stop  = (Button) findViewById(R.id.btnStop);
        start.setOnClickListener(new View.OnClickListener() {
            @Override public void onClick(View v) {
                startService(new Intent(MainActivity.this, StreamService.class));
                info.setText("Streaming on http://<GLASS_IP>:8080/stream.mjpeg");
            }
        });
        stop.setOnClickListener(new View.OnClickListener() {
            @Override public void onClick(View v) {
                stopService(new Intent(MainActivity.this, StreamService.class));
                info.setText("Stopped");
            }
        });
    }
}
