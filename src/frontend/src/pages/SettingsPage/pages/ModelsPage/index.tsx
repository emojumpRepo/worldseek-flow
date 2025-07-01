import IconComponent, {
  ForwardedIconComponent,
} from "../../../../components/common/genericIconComponent";
import { Button } from "../../../../components/ui/button";

import ModelModal from "@/components/core/ModelModal/ModelModal";
import TableComponent from "@/components/core/parameterRenderComponent/components/tableComponent";
import {
  useDeleteModel,
  useGetModels,
  Model,
} from "@/controllers/API/queries/models/use-models-crud";
import {
  ColDef,
  RowClickedEvent,
  SelectionChangedEvent,
} from "ag-grid-community";
import { useRef, useState } from "react";
import useAlertStore from "../../../../stores/alertStore";
  
export default function ModelsPage() {
  const setErrorData = useAlertStore((state) => state.setErrorData);
  const [openModal, setOpenModal] = useState(false);
  const initialData = useRef<Model | undefined>(undefined);

  // Column Definitions: Defines the columns to be displayed.
  const colDefs: ColDef[] = [
    {
      headerName: "名称",
      field: "name",
      flex: 2,
    },
    {
      headerName: "模型配置",
      field: "config",
      flex: 1,
      cellRenderer: () => (
        <div className="flex h-full items-center">
          <span className="text-sm text-muted-foreground">管理</span>
        </div>
      ),
    },
  ];

  const [selectedRows, setSelectedRows] = useState<string[]>([]);

  const { data: models } = useGetModels();
  const { mutate: mutateDeleteModel } = useDeleteModel();

  async function removeModels() {
    selectedRows.map(async (rowName) => {
      const model = models?.find((m) => m.name === rowName);
      if (model?.id) {
        mutateDeleteModel(
          model.id,
          {
            onError: () => {
              setErrorData({
                title: `删除模型失败`,
                list: [`未找到对应ID的模型: ${rowName}`],
              });
            },
          }
        );
      }
    });
  }

  function updateModel(event: RowClickedEvent<Model>) {
    initialData.current = event.data;
    setOpenModal(true);
  }

  return (
    <div className="flex h-full w-full flex-col justify-between gap-6">
      <div className="flex w-full items-start justify-between gap-6">
        <div className="flex w-full flex-col">
          <h2 className="flex items-center text-lg font-semibold tracking-tight">
            模型
            <ForwardedIconComponent
              name="models"
              className="ml-2 h-5 w-5 text-primary"
            />
          </h2>
          <p className="text-sm text-muted-foreground">
            管理 WorldSeek Agent 中的模型配置
          </p>
        </div>
        <div className="flex flex-shrink-0 items-center gap-2">
          <ModelModal asChild>
            <Button data-testid="add-model-button" variant="primary">
              <IconComponent name="Plus" className="w-4" />
              添加模型
            </Button>
          </ModelModal>
        </div>
      </div>

      <div className="flex h-full w-full flex-col justify-between">
        <TableComponent
          key={"models"}
          overlayNoRowsTemplate="没有数据"
          onSelectionChanged={(event: SelectionChangedEvent) => {
            setSelectedRows(event.api.getSelectedRows().map((row) => row.name));
          }}
          rowSelection="multiple"
          onRowClicked={updateModel}
          suppressRowClickSelection={true}
          pagination={true}
          columnDefs={colDefs}
          rowData={models ?? []}
          onDelete={removeModels}
        />
        {initialData.current && (
          <ModelModal
            key={initialData.current.id}
            initialData={initialData.current}
            open={openModal}
            setOpen={setOpenModal}
          />
        )}
      </div>
    </div>
  );
}
  