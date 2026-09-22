import java.io.InputStream;
import java.nio.charset.StandardCharsets;
import java.nio.file.Files;
import java.nio.file.Path;
import java.nio.file.StandardOpenOption;
import java.security.Key;
import java.security.KeyStore;
import java.security.PrivateKey;
import java.util.Arrays;
import java.util.Base64;
import java.util.Enumeration;

public final class ExportPrivateKey {
    private ExportPrivateKey() {}

    public static void main(String[] args) throws Exception {
        if (args.length != 2) {
            throw new IllegalArgumentException(
                    "Usage: ExportPrivateKey <PKCS12 file> <PEM output>");
        }

        String passwordValue = System.getenv("TRINO_CLIENT_STORE_PASSWORD");
        if (passwordValue == null || passwordValue.isEmpty()) {
            throw new IllegalStateException(
                    "TRINO_CLIENT_STORE_PASSWORD must be set");
        }

        char[] password = passwordValue.toCharArray();
        try {
            KeyStore keyStore = KeyStore.getInstance("PKCS12");
            try (InputStream input = Files.newInputStream(Path.of(args[0]))) {
                keyStore.load(input, password);
            }

            String keyAlias = findKeyAlias(keyStore);
            Key key = keyStore.getKey(keyAlias, password);
            if (!(key instanceof PrivateKey)) {
                throw new IllegalStateException(
                        "PKCS12 key entry is not a private key: " + keyAlias);
            }
            PrivateKey privateKey = (PrivateKey) key;

            Base64.Encoder encoder = Base64.getMimeEncoder(
                    64, "\n".getBytes(StandardCharsets.US_ASCII));
            String pem = "-----BEGIN PRIVATE KEY-----\n"
                    + encoder.encodeToString(privateKey.getEncoded())
                    + "\n-----END PRIVATE KEY-----\n";
            Files.writeString(
                    Path.of(args[1]),
                    pem,
                    StandardCharsets.US_ASCII,
                    StandardOpenOption.CREATE_NEW,
                    StandardOpenOption.WRITE);
        }
        finally {
            Arrays.fill(password, '\0');
        }
    }

    private static String findKeyAlias(KeyStore keyStore) throws Exception {
        Enumeration<String> aliases = keyStore.aliases();
        while (aliases.hasMoreElements()) {
            String alias = aliases.nextElement();
            if (keyStore.isKeyEntry(alias)) {
                return alias;
            }
        }
        throw new IllegalStateException("PKCS12 store contains no key entry");
    }
}
