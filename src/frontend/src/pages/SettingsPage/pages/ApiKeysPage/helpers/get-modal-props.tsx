export const getModalPropsApiKey = () => {
  const modalProps = {
    title: "生成API密钥",
    description: "生成一个API密钥来调用WorldSeek Agent API。",
    inputPlaceholder: "我的API密钥",
    buttonText: "生成API密钥",
    generatedKeyMessage: (
      <>
        请将此密钥保存到安全且可访问的地方。出于安全原因，<strong>您将无法通过您的账户再次查看它。</strong>如果您丢失此密钥，您需要生成一个新的密钥。
      </>
    ),
    showIcon: true,
    inputLabel: (
      <>
        <span className="text-sm">描述</span>
        <span className="text-xs text-muted-foreground">(可选)</span>
      </>
    ),
  };

  return modalProps;
};
