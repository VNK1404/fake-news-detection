"use client";

import { create } from "zustand";
import type { AnalysisResult, AnalyticsPayload } from "@/lib/api";

type ThemeMode = "dark" | "light";

interface AppState {
  theme: ThemeMode;
  uploadFileName: string | null;
  isAnalyzing: boolean;
  currentAnalysis: AnalysisResult | null;
  analyticsCache: AnalyticsPayload | null;
  setTheme: (theme: ThemeMode) => void;
  setUploadFileName: (fileName: string | null) => void;
  setAnalyzing: (isAnalyzing: boolean) => void;
  setCurrentAnalysis: (analysis: AnalysisResult | null) => void;
  setAnalyticsCache: (payload: AnalyticsPayload | null) => void;
}

export const useAppStore = create<AppState>((set) => ({
  theme: "dark",
  uploadFileName: null,
  isAnalyzing: false,
  currentAnalysis: null,
  analyticsCache: null,
  setTheme: (theme) => set({ theme }),
  setUploadFileName: (uploadFileName) => set({ uploadFileName }),
  setAnalyzing: (isAnalyzing) => set({ isAnalyzing }),
  setCurrentAnalysis: (currentAnalysis) => set({ currentAnalysis }),
  setAnalyticsCache: (analyticsCache) => set({ analyticsCache }),
}));
