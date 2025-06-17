import ForwardedIconComponent from "../../../../../../components/common/genericIconComponent";

const HeaderMessagesComponent = () => {
  return (
    <>
      <div className="flex w-full items-center justify-between gap-4 space-y-0.5">
        <div className="flex w-full flex-col">
          <h2 className="flex items-center text-lg font-semibold tracking-tight">
            消息
            <ForwardedIconComponent
              name="MessagesSquare"
              className="ml-2 h-5 w-5 text-primary"
            />
          </h2>
          <p className="text-sm text-muted-foreground">
            查看、编辑和删除消息以探索和细化模型行为。
          </p>
        </div>
      </div>
    </>
  );
};
export default HeaderMessagesComponent;
