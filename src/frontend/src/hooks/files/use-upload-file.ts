import { customPostUploadFileV2 } from "@/customization/hooks/use-custom-post-upload-file";
import { createFileUpload } from "@/helpers/create-file-upload";
import useFileSizeValidator from "@/shared/hooks/use-file-size-validator";

const useUploadFile = ({
  types,
  multiple,
}: {
  types?: string[];
  multiple?: boolean;
}) => {
  const { mutateAsync: uploadFileMutation } = customPostUploadFileV2();
  const { validateFileSize } = useFileSizeValidator();

  const getFilesToUpload = async ({
    files,
  }: {
    files?: File[];
  }): Promise<File[]> => {
    if (!files) {
      files = await createFileUpload({
        accept: types?.map((type) => `.${type}`).join(",") ?? "",
        multiple: multiple ?? false,
      });
    }
    return files;
  };

  const uploadFile = async ({
    files,
  }: {
    files?: File[];
  }): Promise<string[]> => {
    try {
      const filesToUpload = await getFilesToUpload({ files });
      const filesIds: string[] = [];

      for (const file of filesToUpload) {
        validateFileSize(file);
        // Check if file extension is allowed
        const fileExtension = file.name.split(".").pop()?.toLowerCase();
        if (!fileExtension || (types && !types.includes(fileExtension))) {
          throw new Error(
            `文件类型 ${fileExtension} 不允许。允许的类型: ${types?.join(", ")}`,
          );
        }
        if (!fileExtension) {
          throw new Error("文件类型不允许");
        }
        if (!multiple && filesToUpload.length !== 1) {
          throw new Error("不允许上传多个文件");
        }

        const res = await uploadFileMutation({
          file,
        });
        filesIds.push(res.path);
      }
      return filesIds;
    } catch (e) {
      throw e;
    }
  };

  return uploadFile;
};

export default useUploadFile;
