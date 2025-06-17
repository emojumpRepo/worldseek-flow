import CodeAreaModal from "@/modals/codeAreaModal";
import ConfirmationModal from "@/modals/confirmationModal";
import EditNodeModal from "@/modals/editNodeModal";
import ShareModal from "@/modals/shareModal";
import { APIClassType } from "@/types/api";
import { FlowType } from "@/types/flow";
import { memo } from "react";

interface ToolbarModalsProps {
  // Modal visibility states
  showModalAdvanced: boolean;
  showconfirmShare: boolean;
  showOverrideModal: boolean;
  openModal: boolean;
  hasCode: boolean;

  // Setters for modal states
  setShowModalAdvanced: (value: boolean) => void;
  setShowconfirmShare: (value: boolean) => void;
  setShowOverrideModal: (value: boolean) => void;
  setOpenModal: (value: boolean) => void;

  // Data and handlers
  data: any;
  flowComponent: FlowType;
  handleOnNewValue: (value: string | string[]) => void;
  handleNodeClass: (apiClassType: APIClassType, type: string) => void;
  setToolMode: (value: boolean) => void;
  setSuccessData: (data: { title: string }) => void;
  addFlow: (params: { flow: FlowType; override: boolean }) => void;
  name?: string;
}

const ToolbarModals = memo(
  ({
    showModalAdvanced,
    showconfirmShare,
    showOverrideModal,
    openModal,
    hasCode,
    setShowModalAdvanced,
    setShowconfirmShare,
    setShowOverrideModal,
    setOpenModal,
    data,
    flowComponent,
    handleOnNewValue,
    handleNodeClass,
    setToolMode,
    setSuccessData,
    addFlow,
    name = "code",
  }: ToolbarModalsProps) => {
    // Handlers for confirmation modal
    const handleConfirm = () => {
      addFlow({
        flow: flowComponent,
        override: true,
      });
      setSuccessData({ title: `${data.id} 已覆盖！` });
      setShowOverrideModal(false);
    };

    const handleClose = () => {
      setShowOverrideModal(false);
    };

    const handleCancel = () => {
      addFlow({
        flow: flowComponent,
        override: true,
      });
      setSuccessData({ title: "新组件已保存！" });
      setShowOverrideModal(false);
    };

    return (
      <>
        {showModalAdvanced && (
          <EditNodeModal
            data={data}
            open={showModalAdvanced}
            setOpen={setShowModalAdvanced}
          />
        )}

        {showconfirmShare && (
          <ShareModal
            open={showconfirmShare}
            setOpen={setShowconfirmShare}
            is_component={true}
            component={flowComponent}
          />
        )}

        {showOverrideModal && (
          <ConfirmationModal
            open={showOverrideModal}
            title="覆盖"
            onConfirm={handleConfirm}
            onClose={handleClose}
            onCancel={handleCancel}
            cancelText="创建新组件"
            confirmationText="确认覆盖"
            size="x-small"
            icon="SaveAll"
            index={6}
          >
            <ConfirmationModal.Content>
              <span>
                看起来 {data.node?.display_name} 已存在。您想用当前组件覆盖它还是创建一个新组件？
              </span>
            </ConfirmationModal.Content>
          </ConfirmationModal>
        )}

        {hasCode && (
          <div className="hidden">
            {openModal && (
              <CodeAreaModal
                setValue={handleOnNewValue}
                open={openModal}
                setOpen={setOpenModal}
                dynamic={true}
                setNodeClass={(apiClassType, type) => {
                  handleNodeClass(apiClassType, type);
                  setToolMode(false);
                }}
                nodeClass={data.node}
                value={data.node?.template[name]?.value ?? ""}
                componentId={data.id}
              >
                <></>
              </CodeAreaModal>
            )}
          </div>
        )}
      </>
    );
  },
);

ToolbarModals.displayName = "ToolbarModals";

export default ToolbarModals;
