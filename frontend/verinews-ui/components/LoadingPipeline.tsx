"use client";

import { motion } from "framer-motion";
import { pipelineSteps } from "@/lib/data";

export function LoadingPipeline({ compact = false }: { compact?: boolean }) {
  return (
    <div className="rounded-lg border border-outline-variant bg-surface-container-low p-5">
      <div className={compact ? "grid gap-3 sm:grid-cols-2" : "grid gap-3 md:grid-cols-2 xl:grid-cols-5"}>
        {pipelineSteps.map((step, index) => {
          const Icon = step.icon;
          return (
            <motion.div
              key={step.label}
              initial={{ opacity: 0, y: 8 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ delay: index * 0.045 }}
              className="relative flex min-h-16 items-center gap-3 rounded-lg border border-outline-variant/60 bg-background/70 p-3"
            >
              <motion.span
                animate={{ scale: [1, 1.08, 1] }}
                transition={{ duration: 1.8, repeat: Infinity, delay: index * 0.12 }}
                className="grid size-10 shrink-0 place-items-center rounded-lg bg-secondary/12 text-secondary"
              >
                <Icon size={18} />
              </motion.span>
              <div>
                <p className="text-sm font-semibold text-on-surface">{step.label}</p>
                <p className="text-xs text-on-surface-variant">Stage {index + 1}</p>
              </div>
            </motion.div>
          );
        })}
      </div>
    </div>
  );
}
