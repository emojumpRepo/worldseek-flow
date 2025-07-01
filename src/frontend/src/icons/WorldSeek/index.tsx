import { useDarkStore } from "@/stores/darkStore";
import React, { forwardRef } from "react";
import SvgWorldSeekBox from "./WorldSeek";

export const WorldSeekIcon = forwardRef<
  SVGSVGElement,
  React.PropsWithChildren<{}>
>((props, ref) => {
  const isDark = useDarkStore((state) => state.dark);

  return <SvgWorldSeekBox ref={ref} {...props} isDark={isDark} />;
});
