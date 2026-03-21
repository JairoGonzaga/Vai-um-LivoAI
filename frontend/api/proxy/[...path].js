export const config = {
  api: {
    bodyParser: false,
  },
};

function buildTargetUrl(req, backendApiUrl) {
  const rawPath = req.query.path;
  const segments = Array.isArray(rawPath) ? rawPath : rawPath ? [rawPath] : [];
  const normalizedBase = backendApiUrl.replace(/\/+$/, "");
  const query = new URLSearchParams();
  Object.entries(req.query).forEach(([key, value]) => {
    if (key === "path") return;
    if (Array.isArray(value)) {
      value.forEach((item) => query.append(key, String(item)));
      return;
    }
    if (value !== undefined) {
      query.append(key, String(value));
    }
  });
  const queryString = query.toString() ? `?${query.toString()}` : "";
  const suffix = segments.length ? `/${segments.join("/")}` : "";
  return `${normalizedBase}${suffix}${queryString}`;
}

function collectForwardHeaders(req, backendApiKey) {
  const headers = {
    "x-api-key": backendApiKey,
  };

  const contentType = req.headers["content-type"];
  const authorization = req.headers.authorization;
  const xSessionToken = req.headers["x-session-token"];
  const xClientRequestId = req.headers["x-client-request-id"];

  if (contentType) headers["content-type"] = contentType;
  if (authorization) headers.authorization = authorization;
  if (xSessionToken) headers["x-session-token"] = xSessionToken;
  if (xClientRequestId) headers["x-client-request-id"] = xClientRequestId;

  return headers;
}

async function readRawBody(req) {
  const chunks = [];
  for await (const chunk of req) {
    chunks.push(typeof chunk === "string" ? Buffer.from(chunk) : chunk);
  }
  return chunks.length ? Buffer.concat(chunks) : undefined;
}

export default async function handler(req, res) {
  const backendApiUrl = (process.env.BACKEND_API_URL ?? "").trim();
  const backendApiKey = (process.env.BACKEND_API_KEY ?? "").trim();

  if (!backendApiUrl || !backendApiKey) {
    return res.status(500).json({ detail: "Proxy não configurado no servidor." });
  }

  if (req.method === "OPTIONS") {
    res.setHeader("Allow", "GET,POST,DELETE,OPTIONS");
    return res.status(204).end();
  }

  const targetUrl = buildTargetUrl(req, backendApiUrl);

  try {
    const body = req.method === "GET" || req.method === "HEAD" ? undefined : await readRawBody(req);

    const upstreamResponse = await fetch(targetUrl, {
      method: req.method,
      headers: collectForwardHeaders(req, backendApiKey),
      body,
    });

    const contentType = upstreamResponse.headers.get("content-type");
    const requestId = upstreamResponse.headers.get("x-request-id");

    if (contentType) {
      res.setHeader("content-type", contentType);
    }
    if (requestId) {
      res.setHeader("x-request-id", requestId);
    }

    const bytes = Buffer.from(await upstreamResponse.arrayBuffer());
    return res.status(upstreamResponse.status).send(bytes);
  } catch {
    return res.status(502).json({ detail: "Falha ao comunicar com backend." });
  }
}
