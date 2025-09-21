package com.srikanth.glassstream;

import android.app.Activity;
import android.content.Context;
import android.content.Intent;
import android.net.wifi.WifiInfo;
import android.net.wifi.WifiManager;
import android.os.Bundle;
import android.view.View;
import android.widget.Button;
import android.widget.TextView;
import android.widget.Toast;
import java.util.Locale;

import com.srikanth.glassstream.svc.StreamService;

import java.net.Inet4Address;
import java.net.InetAddress;
import java.net.NetworkInterface;
import java.util.Enumeration;

public class MainActivity extends Activity {
    private TextView info;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);

        info  = (TextView) findViewById(R.id.info);
        Button start = (Button) findViewById(R.id.btnStart);
        Button stop  = (Button) findViewById(R.id.btnStop);

        // Show current IP on launch
        updateInfoWithIp(false);

        start.setOnClickListener(new View.OnClickListener() {
            @Override public void onClick(View v) {
                startService(new Intent(MainActivity.this, StreamService.class));
                updateInfoWithIp(true);
            }
        });

        stop.setOnClickListener(new View.OnClickListener() {
            @Override public void onClick(View v) {
                stopService(new Intent(MainActivity.this, StreamService.class));
                info.setText(getString(R.string.stopped));
            }
        });
    }

    private void updateInfoWithIp(boolean streaming) {
        String ip = getDeviceIpv4();
        if (ip == null || "0.0.0.0".equals(ip)) {
            info.setText(streaming
                    ? getString(R.string.no_wifi_streaming)
                    : getString(R.string.no_wifi_ready));
            return;
        }
        String url = "http://" + ip + ":8080/stream.mjpeg";
        info.setText(streaming
                ? getString(R.string.streaming_on, url)
                : getString(R.string.ready_url, url));
    }


    /** Try WifiManager first; fallback to enumerating interfaces (API 19-safe). */
    private String getDeviceIpv4() {
        // WifiManager path (fast)
        try {
            WifiManager wm = (WifiManager) getApplicationContext().getSystemService(Context.WIFI_SERVICE);
            if (wm != null) {
                WifiInfo wi = wm.getConnectionInfo();
                if (wi != null) {
                    int ip = wi.getIpAddress(); // little-endian int
                    if (ip != 0) {
                        return String.format(Locale.US, "%d.%d.%d.%d",
                                (ip & 0xff),
                                (ip >> 8) & 0xff,
                                (ip >> 16) & 0xff,
                                (ip >> 24) & 0xff);

                    }
                }
            }
        } catch (Exception ignored) {}

        // Fallback: iterate interfaces (e.g., "wlan0") and return first non-loopback IPv4
        try {
            for (Enumeration<NetworkInterface> en = NetworkInterface.getNetworkInterfaces();
                 en.hasMoreElements();) {
                NetworkInterface intf = en.nextElement();
                for (Enumeration<InetAddress> addrs = intf.getInetAddresses();
                     addrs.hasMoreElements();) {
                    InetAddress addr = addrs.nextElement();
                    if (!addr.isLoopbackAddress() && addr instanceof Inet4Address) {
                        return addr.getHostAddress();
                    }
                }
            }
        } catch (Exception ignored) {}

        return "0.0.0.0";
    }
}
