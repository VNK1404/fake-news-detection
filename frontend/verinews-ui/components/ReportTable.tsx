"use client";

import { Download, FileText } from "lucide-react";
import { reports } from "@/lib/data";

export function ReportTable() {
  return (
    <div className="overflow-hidden rounded-lg border border-outline-variant bg-surface-container-low">
      <div className="flex items-center justify-between border-b border-outline-variant p-5">
        <div>
          <p className="text-xs font-bold uppercase tracking-[0.16em] text-on-surface-variant">Generated reports</p>
          <h2 className="mt-2 font-geist text-2xl font-semibold text-on-surface">Evidence packages</h2>
        </div>
        <button className="inline-flex items-center gap-2 rounded-lg bg-primary px-4 py-2 text-sm font-bold text-on-primary">
          <Download size={16} />
          Export
        </button>
      </div>
      <div className="overflow-x-auto">
        <table className="w-full min-w-[720px] text-left text-sm">
          <thead className="bg-background/60 text-xs uppercase tracking-[0.12em] text-on-surface-variant">
            <tr>
              <th className="px-5 py-3">Report</th>
              <th className="px-5 py-3">Claim</th>
              <th className="px-5 py-3">Verdict</th>
              <th className="px-5 py-3">Confidence</th>
              <th className="px-5 py-3">Date</th>
            </tr>
          </thead>
          <tbody>
            {reports.map((report) => (
              <tr key={report.id} className="border-t border-outline-variant/50">
                <td className="px-5 py-4 font-semibold text-on-surface">
                  <span className="inline-flex items-center gap-2">
                    <FileText size={16} className="text-primary" />
                    {report.id}
                  </span>
                </td>
                <td className="px-5 py-4 text-on-surface-variant">{report.claim}</td>
                <td className="px-5 py-4">
                  <span className="rounded-full bg-surface-container-high px-2.5 py-1 text-xs font-semibold text-on-surface">{report.verdict}</span>
                </td>
                <td className="px-5 py-4 text-secondary">{report.confidence}%</td>
                <td className="px-5 py-4 text-on-surface-variant">{report.date}</td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  );
}
