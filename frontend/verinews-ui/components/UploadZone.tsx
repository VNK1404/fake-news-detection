"use client";

import { motion } from "framer-motion";
import { FileText, UploadCloud } from "lucide-react";
import { useAppStore } from "@/store/useAppStore";

export function UploadZone() {
  const fileName = useAppStore((state) => state.uploadFileName);
  const setUploadFileName = useAppStore((state) => state.setUploadFileName);

  return (
    <motion.label
      whileHover={{ y: -2 }}
      className="flex min-h-[280px] cursor-pointer flex-col items-center justify-center rounded-lg border border-dashed border-primary/45 bg-surface-container-low p-8 text-center transition hover:border-secondary hover:bg-surface-container"
    >
      <input
        className="sr-only"
        type="file"
        accept=".jpg,.jpeg,.png,.bmp,.pdf"
        onChange={(event) => setUploadFileName(event.target.files?.[0]?.name ?? null)}
      />
      <span className="grid size-16 place-items-center rounded-lg bg-primary/15 text-primary">
        <UploadCloud size={30} />
      </span>
      <h2 className="mt-5 font-geist text-2xl font-semibold text-on-surface">Upload media or evidence file</h2>
      <p className="mt-3 max-w-md text-sm leading-6 text-on-surface-variant">
        Images and PDFs are staged for OCR, claim extraction, semantic matching, and evidence integrity review.
      </p>
      {fileName ? (
        <div className="mt-6 flex items-center gap-2 rounded-lg border border-outline-variant bg-background px-4 py-3 text-sm text-on-surface">
          <FileText size={17} />
          {fileName}
        </div>
      ) : null}
    </motion.label>
  );
}
