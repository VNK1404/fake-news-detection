import {
  BarChart3,
  Database,
  FileCheck2,
  FileText,
  Gauge,
  Home,
  LineChart,
  Microscope,
  Newspaper,
  Radar,
  Settings,
  ShieldCheck,
  UploadCloud,
} from "lucide-react";

export const navItems = [
  { href: "/", label: "Dashboard", icon: Home },
  { href: "/analyze", label: "Analyze", icon: Microscope },
  { href: "/results", label: "Results", icon: ShieldCheck },
  { href: "/analytics", label: "Analytics", icon: BarChart3 },
  { href: "/reports", label: "Reports", icon: FileCheck2 },
  { href: "/settings", label: "Settings", icon: Settings },
];

export const pipelineSteps = [
  { label: "Upload", icon: UploadCloud },
  { label: "OCR & Cleaning", icon: FileText },
  { label: "Claim Extraction", icon: Newspaper },
  { label: "RoBERTa", icon: Microscope },
  { label: "FAISS", icon: Database },
  { label: "Fact Verification", icon: Radar },
  { label: "Source Credibility", icon: Gauge },
  { label: "Explainability", icon: LineChart },
  { label: "Final Verdict", icon: ShieldCheck },
  { label: "PDF Report", icon: FileCheck2 },
];

export const similarClaims = [
  { title: "WHO confirms vaccine safety after global study", score: 0.94, verdict: "Verified" },
  { title: "Misleading claim about climate satellite imagery", score: 0.88, verdict: "False" },
  { title: "Election commission rejects viral polling rumor", score: 0.82, verdict: "Questionable" },
];

export const analyticsSeries = [
  { day: "Mon", real: 42, false: 18, uncertain: 11 },
  { day: "Tue", real: 49, false: 22, uncertain: 13 },
  { day: "Wed", real: 61, false: 28, uncertain: 17 },
  { day: "Thu", real: 57, false: 24, uncertain: 19 },
  { day: "Fri", real: 74, false: 31, uncertain: 16 },
  { day: "Sat", real: 69, false: 27, uncertain: 12 },
  { day: "Sun", real: 81, false: 33, uncertain: 15 },
];

export const reports = [
  { id: "VRN-2401", claim: "Central bank confirms emergency rate cut", verdict: "Verified", confidence: 94, date: "Today" },
  { id: "VRN-2402", claim: "Fabricated celebrity endorsement circulates", verdict: "False", confidence: 91, date: "Today" },
  { id: "VRN-2403", claim: "Regional weather warning shared without source", verdict: "Questionable", confidence: 68, date: "Yesterday" },
  { id: "VRN-2404", claim: "Research paper misquoted in viral thread", verdict: "False", confidence: 87, date: "Yesterday" },
];

export const healthSignals = [
  { label: "RoBERTa", status: "Operational", value: "42 ms" },
  { label: "FAISS Index", status: "Operational", value: "18 ms" },
  { label: "Fact APIs", status: "Degraded", value: "2.3 s" },
  { label: "PDF Reports", status: "Operational", value: "Ready" },
];

export const trustSignals = [
  { label: "Source Credibility", value: 82 },
  { label: "Semantic Consensus", value: 74 },
  { label: "Fact Check Coverage", value: 68 },
  { label: "Model Certainty", value: 91 },
];

export const evidenceItems = [
  "RoBERTa classified the claim as high-risk misinformation.",
  "FAISS found three semantically similar claims with verified labels.",
  "Source scoring found one high-trust and one low-trust domain in supporting evidence.",
  "Explainability layer weighted model and source signals as the strongest contributors.",
];
