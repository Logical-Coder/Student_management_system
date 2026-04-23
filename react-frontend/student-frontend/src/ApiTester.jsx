import { useState } from "react";
import axios from "axios";

const METHODS = ["GET", "POST", "PUT", "PATCH", "DELETE"];

const METHOD_COLORS = {
  GET: "#10b981",
  POST: "#3b82f6",
  PUT: "#f59e0b",
  PATCH: "#8b5cf6",
  DELETE: "#ef4444",
};

export default function ApiTester() {
  const [baseUrl, setBaseUrl] = useState("");
  const [method, setMethod] = useState("GET");
  const [jsonBody, setJsonBody] = useState("");
  const [jsonError, setJsonError] = useState("");
  const [response, setResponse] = useState(null);
  const [loading, setLoading] = useState(false);
  const [status, setStatus] = useState(null);
  const [statusText, setStatusText] = useState("");
  const [responseTime, setResponseTime] = useState(null);

  const validateJson = (value) => {
    if (!value.trim()) {
      setJsonError("");
      return true;
    }
    try {
      JSON.parse(value);
      setJsonError("");
      return true;
    } catch (e) {
      setJsonError("Invalid JSON: " + e.message);
      return false;
    }
  };

  const handleJsonChange = (e) => {
    setJsonBody(e.target.value);
    validateJson(e.target.value);
  };

  const formatJson = () => {
    try {
      const parsed = JSON.parse(jsonBody);
      setJsonBody(JSON.stringify(parsed, null, 2));
      setJsonError("");
    } catch (e) {
      setJsonError("Cannot format — Invalid JSON: " + e.message);
    }
  };

  const handleSend = async () => {
    if (!baseUrl.trim()) return;
    if (jsonBody.trim() && !validateJson(jsonBody)) return;

    setLoading(true);
    setResponse(null);
    setStatus(null);
    setStatusText("");
    setResponseTime(null);

    const startTime = performance.now();

    try {
      const config = {
        method: method.toLowerCase(),
        url: baseUrl,
        headers: { "Content-Type": "application/json" },
      };

      if (["POST", "PUT", "PATCH"].includes(method) && jsonBody.trim()) {
        config.data = JSON.parse(jsonBody);
      }

      const res = await axios(config);
      const elapsed = Math.round(performance.now() - startTime);

      setStatus(res.status);
      setStatusText(res.statusText);
      setResponseTime(elapsed);
      setResponse(JSON.stringify(res.data, null, 2));
    } catch (err) {
      const elapsed = Math.round(performance.now() - startTime);
      setResponseTime(elapsed);

      if (err.response) {
        setStatus(err.response.status);
        setStatusText(err.response.statusText);
        setResponse(JSON.stringify(err.response.data, null, 2));
      } else {
        setStatus("ERR");
        setStatusText("Network Error");
        setResponse(err.message);
      }
    } finally {
      setLoading(false);
    }
  };

  const getStatusColor = (code) => {
    if (code >= 200 && code < 300) return "#10b981";
    if (code >= 300 && code < 400) return "#f59e0b";
    if (code >= 400) return "#ef4444";
    return "#94a3b8";
  };

  return (
    <div style={styles.wrapper}>
      {/* Header */}
      <div style={styles.header}>
        <span style={styles.headerIcon}>⚡</span>
        <h2 style={styles.headerTitle}>API Tester</h2>
        <span style={styles.headerSub}>Test your REST endpoints</span>
      </div>

      {/* URL Bar */}
      <div style={styles.urlBar}>
        {/* Method Selector */}
        <select
          id="method-select"
          value={method}
          onChange={(e) => setMethod(e.target.value)}
          style={{
            ...styles.methodSelect,
            color: METHOD_COLORS[method],
            borderColor: METHOD_COLORS[method] + "60",
            background: METHOD_COLORS[method] + "12",
          }}
        >
          {METHODS.map((m) => (
            <option key={m} value={m} style={{ color: METHOD_COLORS[m] }}>
              {m}
            </option>
          ))}
        </select>

        {/* URL Input */}
        <input
          id="base-url-input"
          type="text"
          placeholder="https://api.example.com/endpoint"
          value={baseUrl}
          onChange={(e) => setBaseUrl(e.target.value)}
          onKeyDown={(e) => e.key === "Enter" && handleSend()}
          style={styles.urlInput}
        />

        {/* Send Button */}
        <button
          id="send-btn"
          onClick={handleSend}
          disabled={loading || !baseUrl.trim()}
          style={{
            ...styles.sendBtn,
            background: loading ? "#475569" : `linear-gradient(135deg, ${METHOD_COLORS[method]}, ${METHOD_COLORS[method]}cc)`,
            cursor: loading || !baseUrl.trim() ? "not-allowed" : "pointer",
            opacity: !baseUrl.trim() ? 0.5 : 1,
          }}
        >
          {loading ? (
            <span style={styles.spinner}>⏳</span>
          ) : (
            "Send"
          )}
        </button>
      </div>

      {/* Body Section — shown only for POST/PUT/PATCH */}
      <div style={styles.bodySection}>
        <div style={styles.sectionHeader}>
          <span style={styles.sectionLabel}>
            Request Body
            {!["POST", "PUT", "PATCH"].includes(method) && (
              <span style={styles.disabledBadge}> (not used for {method})</span>
            )}
          </span>
          {["POST", "PUT", "PATCH"].includes(method) && (
            <button
              id="format-json-btn"
              onClick={formatJson}
              style={styles.formatBtn}
              title="Format JSON"
            >
              ✨ Format JSON
            </button>
          )}
        </div>

        <textarea
          id="json-body-input"
          placeholder={`{\n  "key": "value"\n}`}
          value={jsonBody}
          onChange={handleJsonChange}
          disabled={!["POST", "PUT", "PATCH"].includes(method)}
          style={{
            ...styles.jsonTextarea,
            opacity: !["POST", "PUT", "PATCH"].includes(method) ? 0.4 : 1,
            borderColor: jsonError ? "#ef4444" : "#1e293b",
          }}
          spellCheck={false}
        />

        {jsonError && (
          <div style={styles.jsonError}>
            ⚠️ {jsonError}
          </div>
        )}
      </div>

      {/* Response Section */}
      <div style={styles.responseSection}>
        <div style={styles.responseSectionHeader}>
          <span style={styles.sectionLabel}>Response</span>

          {status !== null && (
            <div style={styles.responseMeta}>
              <span
                style={{
                  ...styles.statusBadge,
                  background: getStatusColor(status) + "20",
                  color: getStatusColor(status),
                  border: `1px solid ${getStatusColor(status)}40`,
                }}
              >
                {status} {statusText}
              </span>
              {responseTime !== null && (
                <span style={styles.timeBadge}>⏱ {responseTime}ms</span>
              )}
            </div>
          )}
        </div>

        <textarea
          id="response-output"
          readOnly
          value={
            loading
              ? "Sending request..."
              : response !== null
              ? response
              : "Response will appear here after you send a request."
          }
          style={{
            ...styles.responseTextarea,
            color:
              status !== null
                ? getStatusColor(status)
                : "#64748b",
          }}
          spellCheck={false}
        />

        {response !== null && !loading && (
          <button
            id="copy-response-btn"
            onClick={() => navigator.clipboard.writeText(response)}
            style={styles.copyBtn}
          >
            📋 Copy Response
          </button>
        )}
      </div>
    </div>
  );
}

const styles = {
  wrapper: {
    background: "#0f172a",
    minHeight: "100vh",
    padding: "24px",
    boxSizing: "border-box",
    fontFamily: "'Inter', 'Segoe UI', sans-serif",
    color: "#e2e8f0",
  },

  // Header
  header: {
    display: "flex",
    alignItems: "center",
    gap: "10px",
    marginBottom: "24px",
    paddingBottom: "16px",
    borderBottom: "1px solid #1e293b",
  },
  headerIcon: { fontSize: "24px" },
  headerTitle: {
    margin: 0,
    fontSize: "22px",
    fontWeight: "700",
    background: "linear-gradient(135deg, #38bdf8, #818cf8)",
    WebkitBackgroundClip: "text",
    WebkitTextFillColor: "transparent",
  },
  headerSub: {
    marginLeft: "auto",
    fontSize: "13px",
    color: "#475569",
  },

  // URL Bar
  urlBar: {
    display: "flex",
    gap: "10px",
    marginBottom: "20px",
    alignItems: "center",
  },
  methodSelect: {
    padding: "12px 14px",
    borderRadius: "10px",
    border: "1.5px solid",
    fontSize: "13px",
    fontWeight: "700",
    cursor: "pointer",
    outline: "none",
    minWidth: "110px",
    letterSpacing: "0.5px",
    transition: "all 0.2s",
  },
  urlInput: {
    flex: 1,
    padding: "12px 16px",
    borderRadius: "10px",
    border: "1.5px solid #1e293b",
    background: "#1e293b",
    color: "#e2e8f0",
    fontSize: "14px",
    outline: "none",
    transition: "border 0.2s",
    fontFamily: "'Fira Code', 'Courier New', monospace",
    letterSpacing: "0.3px",
  },
  sendBtn: {
    padding: "12px 28px",
    borderRadius: "10px",
    border: "none",
    color: "#fff",
    fontWeight: "700",
    fontSize: "14px",
    letterSpacing: "0.5px",
    transition: "all 0.2s",
    minWidth: "90px",
    boxShadow: "0 4px 15px rgba(0,0,0,0.3)",
  },
  spinner: { fontSize: "16px" },

  // Body Section
  bodySection: {
    background: "#1e293b",
    borderRadius: "12px",
    padding: "16px",
    marginBottom: "20px",
    border: "1px solid #334155",
  },
  sectionHeader: {
    display: "flex",
    justifyContent: "space-between",
    alignItems: "center",
    marginBottom: "10px",
  },
  sectionLabel: {
    fontSize: "12px",
    fontWeight: "700",
    textTransform: "uppercase",
    letterSpacing: "1px",
    color: "#94a3b8",
  },
  disabledBadge: {
    fontWeight: "400",
    textTransform: "none",
    color: "#475569",
    fontSize: "11px",
    letterSpacing: "0",
  },
  formatBtn: {
    padding: "5px 12px",
    borderRadius: "6px",
    border: "1px solid #334155",
    background: "#0f172a",
    color: "#94a3b8",
    fontSize: "12px",
    cursor: "pointer",
    transition: "all 0.2s",
  },
  jsonTextarea: {
    width: "100%",
    minHeight: "160px",
    background: "#0f172a",
    color: "#a5f3fc",
    border: "1.5px solid #1e293b",
    borderRadius: "8px",
    padding: "14px",
    fontSize: "13px",
    fontFamily: "'Fira Code', 'Courier New', monospace",
    resize: "vertical",
    outline: "none",
    lineHeight: "1.7",
    boxSizing: "border-box",
    transition: "border 0.2s",
  },
  jsonError: {
    marginTop: "8px",
    color: "#ef4444",
    fontSize: "12px",
    background: "#ef444415",
    padding: "8px 12px",
    borderRadius: "6px",
    border: "1px solid #ef444430",
  },

  // Response Section
  responseSection: {
    background: "#1e293b",
    borderRadius: "12px",
    padding: "16px",
    border: "1px solid #334155",
  },
  responseSectionHeader: {
    display: "flex",
    justifyContent: "space-between",
    alignItems: "center",
    marginBottom: "10px",
  },
  responseMeta: {
    display: "flex",
    gap: "8px",
    alignItems: "center",
  },
  statusBadge: {
    padding: "4px 10px",
    borderRadius: "20px",
    fontSize: "12px",
    fontWeight: "700",
    letterSpacing: "0.5px",
  },
  timeBadge: {
    padding: "4px 10px",
    borderRadius: "20px",
    fontSize: "12px",
    background: "#0f172a",
    color: "#64748b",
    border: "1px solid #334155",
  },
  responseTextarea: {
    width: "100%",
    minHeight: "280px",
    background: "#0f172a",
    border: "1.5px solid #1e293b",
    borderRadius: "8px",
    padding: "14px",
    fontSize: "13px",
    fontFamily: "'Fira Code', 'Courier New', monospace",
    resize: "vertical",
    outline: "none",
    lineHeight: "1.7",
    boxSizing: "border-box",
  },
  copyBtn: {
    marginTop: "10px",
    padding: "7px 14px",
    borderRadius: "7px",
    border: "1px solid #334155",
    background: "#0f172a",
    color: "#94a3b8",
    fontSize: "12px",
    cursor: "pointer",
    transition: "all 0.2s",
    float: "right",
  },
};
