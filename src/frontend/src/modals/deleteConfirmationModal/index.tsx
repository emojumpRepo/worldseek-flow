import { DialogClose } from "@radix-ui/react-dialog";
import { Trash2 } from "lucide-react";
import { Button } from "../../components/ui/button";
import {
  Dialog,
  DialogContent,
  DialogFooter,
  DialogHeader,
  DialogTitle,
  DialogTrigger,
} from "../../components/ui/dialog";

export default function DeleteConfirmationModal({
  children,
  onConfirm,
  description,
  asChild,
  open,
  setOpen,
  note = "",
}: {
  children?: JSX.Element;
  onConfirm: (e: React.MouseEvent<HTMLButtonElement, MouseEvent>) => void;
  description?: string;
  asChild?: boolean;
  open?: boolean;
  setOpen?: (open: boolean) => void;
  note?: string;
}) {
  return (
    <Dialog open={open} onOpenChange={setOpen}>
      <DialogTrigger asChild={!children ? true : asChild} tabIndex={-1}>
        {children ?? <></>}
      </DialogTrigger>
      <DialogContent>
        <DialogHeader>
          <DialogTitle>
            <div className="flex items-center">
              <Trash2
                className="h-6 w-6 pr-1 text-foreground"
                strokeWidth={1.5}
              />
              <span className="pl-2">删除</span>
            </div>
          </DialogTitle>
        </DialogHeader>
        <span className="pb-3 text-sm">
          这将永久删除该{description ?? "工作流"}
          {note || ""}。<br></br>无法撤销。
        </span>
        <DialogFooter>
          <DialogClose asChild>
            <Button
              onClick={(e) => e.stopPropagation()}
              className="mr-1"
              variant="outline"
              data-testid="btn_cancel_delete_confirmation_modal"
            >
              取消
            </Button>
          </DialogClose>
          <DialogClose asChild>
            <Button
              type="submit"
              variant="destructive"
              onClick={(e) => {
                onConfirm(e);
              }}
              data-testid="btn_delete_delete_confirmation_modal"
            >
              删除
            </Button>
          </DialogClose>
        </DialogFooter>
      </DialogContent>
    </Dialog>
  );
}
