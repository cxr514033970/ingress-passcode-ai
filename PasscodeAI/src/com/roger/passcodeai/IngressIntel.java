package com.roger.passcodeai;

import java.io.IOException;
import java.net.HttpURLConnection;
import java.net.MalformedURLException;
import java.net.URL;

import android.content.Context;
import android.util.Log;
import android.webkit.CookieManager;
import android.webkit.CookieSyncManager;

public class IngressIntel {
    private static final String URL_INGRESS ="http://www.ingress.com/intel";
    private static final String URL_LOGIN = "https://accounts.google.com/ServiceLogin?service=grandcentral";
    private static final String URL_AUTHENTICATE = "https://accounts.google.com/ServiceLoginAuth";
    private static final String URL_PASSCODE = "http://www.ingress.com/rpc/dashboard.redeemReward";
    
    private final String mUsername, mPasswd;
    private final Context mContext;
    public IngressIntel(Context context, String username, String password) {
        mContext = context.getApplicationContext();
        mUsername = username;
        mPasswd = password;
    }
    
    public void login() {
        Log.d("Debug", "login");
        URL url;
        try {
            url = new URL(URL_INGRESS);
            HttpURLConnection httpUrlConn = (HttpURLConnection) url.openConnection();  
            httpUrlConn.setRequestProperty("cookie", getCookie(mContext));
            httpUrlConn.connect();
            int code = httpUrlConn.getResponseCode();
            if (code != 200) {
                Log.d("Debug", "code = " + code);
                throw new IOException("HTTP error: " + code);
            } else {
                Log.d("Debug", "code = " + code);
            }
        } catch (MalformedURLException e) {
            e.printStackTrace();
        } catch (IOException e) {
            e.printStackTrace();
        }  
    }
    
    public String getCookie(Context context) {
        CookieSyncManager.createInstance(mContext);
        CookieManager cookieManager = CookieManager.getInstance();
        String cookie = cookieManager.getCookie("cookie");
        if (cookie != null) {
            return cookie;
        } else {
            cookie = "XXX";
            cookieManager.setCookie("cookie", cookie);
            return cookie;
        }
    }
}
