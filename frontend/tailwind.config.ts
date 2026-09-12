import type { Config } from "tailwindcss";

import { colors, radii } from "./src/lib/constants/tokens";

export default {
  content: ["./src/**/*.{ts,tsx}"],
  theme: {
    extend: {
      colors: {
        ink: colors.ink,
        muted: colors.muted,
        line: colors.line,
        canvas: colors.canvas,
        brand: { DEFAULT: colors.brand, soft: colors.brandSoft },
      },
      borderRadius: radii,
      fontFamily: {
        sans: ["var(--font-sans)", "system-ui", "sans-serif"],
      },
    },
  },
  plugins: [],
} satisfies Config;
