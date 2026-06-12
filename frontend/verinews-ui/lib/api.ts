export type Verdict = "Verified" | "False" | "Questionable" | "Uncertain";

export interface SimilarClaim {
  title: string;
  score: number;
  verdict?: string;
}

export interface AnalysisResult {
  analysisId?: string;
  claim: string;
  finalDecision: Verdict | string;
  confidence: string;
  score: number;
  similarClaims?: SimilarClaim[];
  reasons?: string[];
}

export interface AnalyticsSummary {
  total_analyses: number;
  real_count: number;
  fake_count: number;
  uncertain_count: number;
  average_confidence: number;
  average_latency: number;
}

export interface AnalyticsPerformance {
  average_pipeline_duration: number;
  average_api_duration: number;
  average_similarity_duration: number;
  average_roberta_duration: number;
  latency_trend: Array<Record<string, number | string>>;
}

export interface AnalyticsPayload {
  summary: AnalyticsSummary;
  performance: AnalyticsPerformance;
}

const API_URL = process.env.NEXT_PUBLIC_API_URL ?? "http://127.0.0.1:5000";

async function request<T>(path: string, init?: RequestInit): Promise<T> {
  const response = await fetch(`${API_URL}${path}`, {
    ...init,
    headers: {
      ...(init?.body instanceof FormData ? {} : { "Content-Type": "application/json" }),
      ...init?.headers,
    },
  });

  if (!response.ok) {
    throw new Error(`API request failed: ${response.status} ${response.statusText}`);
  }

  return response.json() as Promise<T>;
}

export function analyzeNews(formData: FormData): Promise<AnalysisResult> {
  return request<AnalysisResult>("/analyze", {
    method: "POST",
    body: formData,
  });
}

export async function downloadReport(analysisId: string): Promise<Blob> {
  const response = await fetch(`${API_URL}/download_report?analysis_id=${encodeURIComponent(analysisId)}`);
  if (!response.ok) {
    throw new Error(`Report download failed: ${response.status} ${response.statusText}`);
  }
  return response.blob();
}

export function getAnalytics(): Promise<AnalyticsPayload> {
  return request<AnalyticsPayload>("/api/analytics");
}

export function getAnalyticsSummary(): Promise<AnalyticsSummary> {
  return request<AnalyticsSummary>("/api/analytics/summary");
}

export function getAnalyticsPerformance(): Promise<AnalyticsPerformance> {
  return request<AnalyticsPerformance>("/api/analytics/performance");
}
