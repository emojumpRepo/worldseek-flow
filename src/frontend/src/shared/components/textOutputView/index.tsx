import { Textarea } from "../../../components/ui/textarea";

const TextOutputView = ({
  left,
  value,
}: {
  left: boolean | undefined;
  value: any;
}) => {
  if (typeof value === "object" && Object.keys(value).includes("text")) {
    value = value.text;
  }

  const isTruncated = value?.length > 20000;

  return (
    <>
      {" "}
      <Textarea
        className={`w-full custom-scroll ${left ? "min-h-32" : "h-full"}`}
        placeholder={"Empty"}
        readOnly
        // update to real value on flowPool
        value={value}
      />
      {isTruncated && (
        <div className="mt-2 text-xs text-muted-foreground">
          由于输出内容过长，已被截断。
        </div>
      )}
    </>
  );
};

export default TextOutputView;
