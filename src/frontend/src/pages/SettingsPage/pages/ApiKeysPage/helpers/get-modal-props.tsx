export const getModalPropsApiKey = () => {
  const modalProps = {
    title: "Create API Key",
    description: "Create a secret API Key to use WorldSeek Agent API.",
    inputPlaceholder: "My API Key",
    buttonText: "Generate API Key",
    generatedKeyMessage: (
      <>
        {" "}
        请将此密钥保存到安全且可访问的地方。出于安全原因，<strong>您将无法通过您的账户再次查看它。</strong>如果您丢失此密钥，您需要生成一个新的密钥。
      </>
    ),
    showIcon: true,
    inputLabel: (
      <>
        <span className="text-sm">描述</span>{" "}
        <span className="text-xs text-muted-foreground">(optional)</span>
      </>
    ),
  };

  return modalProps;
};
