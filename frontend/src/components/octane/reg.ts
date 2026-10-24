import type { Reg } from "@/lib/octane-data";

const MAP: Record<Reg, string> = {
  "UN R148": "bg-reg-1",
  "UN R48": "bg-reg-2",
  "UN R150": "bg-reg-3",
  "UN R10": "bg-reg-4",
};
export const regColor = (r: Reg) => MAP[r];
