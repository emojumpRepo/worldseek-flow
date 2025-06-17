import ForwardedIconComponent from "@/components/common/genericIconComponent";
import TableComponent from "@/components/core/parameterRenderComponent/components/tableComponent";
import { Checkbox } from "@/components/ui/checkbox";
import useDuplicateFlows from "@/pages/MainPage/hooks/use-handle-duplicate";
import useFlowStore from "@/stores/flowStore";
import { ComponentsToUpdateType } from "@/types/zustand/flow";
import { cn } from "@/utils/utils";
import { ColDef } from "ag-grid-community";
import { AgGridReact } from "ag-grid-react";
import { useEffect, useRef, useState } from "react";
import BaseModal from "../baseModal";

export default function UpdateComponentModal({
  open,
  setOpen,
  onUpdateNode,
  children,
  components,
  isMultiple = false,
}: {
  open: boolean;
  setOpen: (open: boolean) => void;
  onUpdateNode: (updatedComponents?: string[]) => void;
  children?: React.ReactNode;
  components: ComponentsToUpdateType[];
  isMultiple?: boolean;
}) {
  const [backupFlow, setBackupFlow] = useState<boolean>(true);
  const [loading, setLoading] = useState<boolean>(false);
  const [selectedComponents, setSelectedComponents] = useState<Set<string>>(
    new Set(components.filter((c) => !c.breakingChange).map((c) => c.id)),
  );
  const agGrid = useRef<AgGridReact>(null);
  const currentFlow = useFlowStore((state) => state.currentFlow);

  const { handleDuplicate } = useDuplicateFlows({
    flow: currentFlow
      ? { ...currentFlow, name: currentFlow.name + " (副本)" }
      : undefined,
  });

  const handleUpdate = () => {
    setLoading(true);
    if (backupFlow) {
      handleDuplicate().then(() => {
        onUpdateNode(
          components.length > 0 ? Array.from(selectedComponents) : undefined,
        );
        setLoading(false);
        setOpen(false);
      });
    } else {
      onUpdateNode(
        components.length > 0 ? Array.from(selectedComponents) : undefined,
      );
      setLoading(false);
      setOpen(false);
    }
  };

  const columnDefs: ColDef[] = [
    { field: "id", hide: true },
    {
      headerName: "组件",
      field: "display_name",
      headerClass: "!text-mmd !font-normal",
      flex: 1,
      headerCheckboxSelection: true,
      checkboxSelection: true,
      resizable: false,
      cellRenderer: (params) => {
        return (
          <div className="flex items-center gap-3">
            {params.data.icon && (
              <ForwardedIconComponent
                name={params.data.icon}
                className="h-4 w-4"
              />
            )}
            {params.value}
          </div>
        );
      },
    },
    {
      headerName: "更新类型",
      field: "breakingChange",
      headerClass: "!text-mmd !font-normal",
      resizable: false,
      flex: 1,
      cellClass: "text-muted-foreground",
      cellRenderer: (params) => {
        return params.value ? (
          <span className="font-semibold text-accent-amber-foreground">
            Breaking
          </span>
        ) : (
          <span>Standard</span>
        );
      },
    },
  ];

  useEffect(() => {
    if (open) {
      setBackupFlow(true);
      setSelectedComponents(
        new Set(components.filter((c) => !c.breakingChange).map((c) => c.id)),
      );
    }
  }, [open]);

  useEffect(() => {
    if (agGrid.current) {
      agGrid.current?.api?.forEachNode((node) => {
        if (selectedComponents.has(node.data.id)) {
          node.setSelected(true);
        } else {
          node.setSelected(false);
        }
      });
    }
  }, [agGrid.current, selectedComponents, open]);

  return (
    <BaseModal
      closeButtonClassName="!top-2 !right-3"
      open={open}
      setOpen={setOpen}
      size="small-update"
      className="px-4 py-3"
    >
      <BaseModal.Trigger asChild>{children ?? <></>}</BaseModal.Trigger>
      <BaseModal.Header>
        <span className="">
          更新{" "}
          {isMultiple ? "组件" : (components?.[0]?.display_name ?? "")}
        </span>
      </BaseModal.Header>
      <BaseModal.Content overflowHidden>
        <div className="flex flex-col gap-6">
          <div className="flex flex-col gap-3 text-sm text-muted-foreground">
            {isMultiple ? (
              <p>
                标记为{" "}
                <span className="font-semibold text-accent-amber-foreground">
                  破坏性的
                </span>{" "}
                的更新可能会改变输入、输出或组件行为。在某些情况下，它们会断开流程中的组件连接，需要您在之后重新检查或重新连接。从侧边栏添加的组件始终使用最新版本。
              </p>
            ) : (
              <>
                <p>
                  此更新可能会改变输入、输出或组件行为。在某些情况下，它将{" "}
                  <span className="font-semibold text-accent-amber-foreground">
                    断开此组件与流程的连接
                  </span>
                  , 需要您在之后重新检查或重新连接。
                </p>
                <p>
                  从侧边栏添加的组件始终使用最新版本。
                </p>
              </>
            )}
          </div>
          {isMultiple && (
            <div className="-mx-4">
              <TableComponent
                columnDefs={columnDefs}
                ref={agGrid}
                domLayout="autoHeight"
                rowData={components}
                rowSelection="multiple"
                className="ag-tool-mode ag-no-selection"
                rowHeight={30}
                headerHeight={30}
                suppressRowClickSelection={false}
                onSelectionChanged={(event) => {
                  const selectedIds = event.api
                    .getSelectedRows()
                    .map((row) => row.id);
                  setSelectedComponents(new Set(selectedIds));
                }}
                suppressRowHoverHighlight={true}
                tableOptions={{ hide_options: true }}
              />
            </div>
          )}
          <div
            className={cn(
              "mb-3 flex items-center gap-3 rounded-md border p-3 text-sm transition-all",
              !backupFlow && "border-accent-amber-foreground bg-accent-amber",
            )}
          >
            <Checkbox
              checked={backupFlow}
              onCheckedChange={(checked) =>
                setBackupFlow(checked === "indeterminate" ? false : checked)
              }
              className="bg-muted"
              id="backupFlow"
              data-testid="backup-flow-checkbox"
            />
            <label htmlFor="backupFlow" className="cursor-pointer select-none">
              更新前请创建备份工作流
            </label>
          </div>
        </div>
      </BaseModal.Content>
      <BaseModal.Footer
        submit={{
          label: "更新组件" + (components.length > 1 ? "s" : ""),
          onClick: handleUpdate,
          disabled: isMultiple && selectedComponents.size === 0,
          loading,
        }}
      ></BaseModal.Footer>
    </BaseModal>
  );
}
