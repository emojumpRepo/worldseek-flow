import TableAutoCellRender from "@/components/core/parameterRenderComponent/components/tableComponent/components/tableAutoCellRender";

export const getColumnDefs = () => {
  return [
    {
      headerCheckboxSelection: true,
      checkboxSelection: true,
      showDisabledCheckboxes: true,
      headerName: "名称",
      field: "name",
      cellRenderer: TableAutoCellRender,
      flex: 2,
    },
    {
      headerName: "密钥",
      field: "api_key",
      cellRenderer: TableAutoCellRender,
      flex: 1,
    },
    {
      headerName: "创建时间",
      field: "created_at",
      cellRenderer: TableAutoCellRender,
      flex: 1,
    },
    {
      headerName: "最近使用时间",
      field: "last_used_at",
      cellRenderer: TableAutoCellRender,
      flex: 1,
    },
    {
      headerName: "总使用次数",
      field: "total_uses",
      cellRenderer: TableAutoCellRender,
      flex: 1,
      resizable: false,
    },
  ];
};
