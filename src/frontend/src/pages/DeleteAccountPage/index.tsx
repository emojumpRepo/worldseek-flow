import LangflowLogo from "@/assets/WorldSeekAgentLogo.svg?react";
import { useState } from "react";
import { Button } from "../../components/ui/button";
import { Input } from "../../components/ui/input";
import BaseModal from "../../modals/baseModal";

export default function DeleteAccountPage() {
  const [showConfirmation, setShowConfirmation] = useState(false);

  const handleDeleteAccount = () => {
    // Implement your account deletion logic here
    // For example, make an API call to delete the account
    // Upon successful deletion, you can redirect the user to another page
    // Implement the logic to redirect the user after account deletion.
    // For example, use react-router-dom's useHistory hook.
  };

  return (
    <div className="flex h-full w-full flex-col items-center justify-center bg-muted">
      <div className="flex w-72 flex-col items-center justify-center gap-2">
        <LangflowLogo
          title="WorldSeek Agent logo"
          className="mb-4 h-10 w-10 scale-[1.5]"
        />
        <span className="mb-4 text-center text-2xl font-semibold text-primary">
          删除您的账户
        </span>
        <Input className="bg-background" placeholder="确认密码" />

        <BaseModal
          open={showConfirmation}
          setOpen={setShowConfirmation}
          size="x-small"
        >
          <BaseModal.Header description="此操作不可撤销，将永久删除您的所有数据和与账户相关的信息。">
            <h3>您确定吗？</h3>
          </BaseModal.Header>
          <BaseModal.Trigger>
            <Button
              variant="default"
              className="w-full hover:bg-status-red"
              onClick={() => setShowConfirmation(true)}
            >
              删除账户
            </Button>
          </BaseModal.Trigger>
          <BaseModal.Content>
            <div className="flex h-full w-full flex-col justify-end">
              <Button
                variant="default"
                className="w-full hover:bg-status-red"
                onClick={() => handleDeleteAccount()}
              >
                删除账户
              </Button>
            </div>
          </BaseModal.Content>
        </BaseModal>
      </div>
    </div>
  );
}
