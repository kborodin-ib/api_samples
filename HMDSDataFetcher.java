import javax.net.ssl.*;
import java.io.BufferedReader;
import java.io.InputStreamReader;
import java.net.URL;
import java.security.cert.X509Certificate;
import java.net.URLEncoder;
import java.nio.charset.StandardCharsets;

public class HMDSDataFetcher {

    public static void hmdsData() {
        try {
            // URL and query parameters
            String baseUrl = "https://localhost:5000/v1/api/hmds/history";
            String conid = "265598";
            String period = "1d";
            String bar = "1min";
            String barType = "Inventory";

            String fullUrl = baseUrl + "?conid=" + URLEncoder.encode(conid, StandardCharsets.UTF_8)
                    + "&period=" + URLEncoder.encode(period, StandardCharsets.UTF_8)
                    + "&bar=" + URLEncoder.encode(bar, StandardCharsets.UTF_8)
                    + "&barType=" + URLEncoder.encode(barType, StandardCharsets.UTF_8);

            // Trust all certificates
            TrustManager[] trustAllCerts = new TrustManager[]{
                new X509TrustManager() {
                    public void checkClientTrusted(X509Certificate[] chain, String authType) {}
                    public void checkServerTrusted(X509Certificate[] chain, String authType) {}
                    public X509Certificate[] getAcceptedIssuers() { return new X509Certificate[0]; }
                }
            };

            SSLContext sc = SSLContext.getInstance("TLS");
            sc.init(null, trustAllCerts, new java.security.SecureRandom());
            HttpsURLConnection.setDefaultSSLSocketFactory(sc.getSocketFactory());

            // Disable hostname verification
            HostnameVerifier allHostsValid = (hostname, session) -> true;
            HttpsURLConnection.setDefaultHostnameVerifier(allHostsValid);

            // Create connection
            URL url = new URL(fullUrl);
            HttpsURLConnection conn = (HttpsURLConnection) url.openConnection();
            conn.setRequestMethod("GET");
            conn.setRequestProperty("Accept", "application/json");

            int responseCode = conn.getResponseCode();
            System.out.println("Response Code: " + responseCode);

            BufferedReader in;
            if (responseCode == 200) {
                in = new BufferedReader(new InputStreamReader(conn.getInputStream()));
            } else {
                in = new BufferedReader(new InputStreamReader(conn.getErrorStream()));
            }

            String inputLine;
            StringBuilder content = new StringBuilder();
            while ((inputLine = in.readLine()) != null) {
                content.append(inputLine).append("\n");
            }
            in.close();

            System.out.println("Response:\n" + content.toString());

            conn.disconnect();

        } catch (Exception e) {
            e.printStackTrace();
        }
    }

    public static void main(String[] args) {
        hmdsData();
    }
}
