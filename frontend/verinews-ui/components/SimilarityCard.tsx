"use client";

import { motion } from "framer-motion";
import { similarClaims } from "@/lib/data";

export function SimilarityCard() {
  return (
    <div className="rounded-lg border border-outline-variant bg-surface-container-low p-5">
      <p className="text-xs font-bold uppercase tracking-[0.16em] text-on-surface-variant">FAISS semantic matches</p>
      <div className="mt-4 space-y-3">
        {similarClaims.map((claim) => (
          <motion.div whileHover={{ x: 3 }} key={claim.title} className="rounded-lg border border-outline-variant/60 bg-background/60 p-4">
            <div className="flex items-start justify-between gap-4">
              <p className="text-sm font-medium leading-6 text-on-surface">{claim.title}</p>
              <span className="shrink-0 rounded-full bg-primary/12 px-2.5 py-1 text-xs font-semibold text-primary">{claim.score.toFixed(2)}</span>
            </div>
            <p className="mt-2 text-xs text-on-surface-variant">{claim.verdict}</p>
          </motion.div>
        ))}
      </div>
    </div>
  );
}
