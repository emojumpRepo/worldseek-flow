import { ForwardedIconComponent } from "@/components/common/genericIconComponent";
import {
  DATASTAX_DOCS_URL,
  DISCORD_URL,
  DOCS_URL,
  GITHUB_URL,
  TWITTER_URL,
} from "@/constants/constants";
import { useLogout } from "@/controllers/API/queries/auth";
import { CustomProfileIcon } from "@/customization/components/custom-profile-icon";
import { ENABLE_DATASTAX_LANGFLOW } from "@/customization/feature-flags";
import { useCustomNavigate } from "@/customization/hooks/use-custom-navigate";
import useAuthStore from "@/stores/authStore";
import { useDarkStore } from "@/stores/darkStore";
import { cn } from "@/utils/utils";
import { FaDiscord, FaGithub, FaTwitter } from "react-icons/fa";
import { useParams } from "react-router-dom";
import {
  HeaderMenu,
  HeaderMenuItemButton,
  HeaderMenuItemLink,
  HeaderMenuItems,
  HeaderMenuToggle,
} from "../HeaderMenu";
import { ProfileIcon } from "../ProfileIcon";
import ThemeButtons from "../ThemeButtons";

export const AccountMenu = () => {
  const { customParam: id } = useParams();
  const version = useDarkStore((state) => state.version);
  const latestVersion = useDarkStore((state) => state.latestVersion);
  const navigate = useCustomNavigate();
  const { mutate: mutationLogout } = useLogout();

  const { isAdmin, autoLogin } = useAuthStore((state) => ({
    isAdmin: state.isAdmin,
    autoLogin: state.autoLogin,
  }));

  const handleLogout = () => {
    mutationLogout();
  };

  const isLatestVersion = version === latestVersion;

  return (
    <>
      <HeaderMenu>
        <HeaderMenuToggle>
          <div
            className="h-6 w-6 rounded-lg focus-visible:outline-0"
            data-testid="user-profile-settings"
          >
            <CustomProfileIcon />
          </div>
        </HeaderMenuToggle>
        <HeaderMenuItems position="right">
          <HeaderMenuItemButton
            onClick={() => {
              navigate("/settings");
            }}
          >
            <span
              data-testid="menu_settings_button"
              id="menu_settings_button"
            >
              设置
            </span>
          </HeaderMenuItemButton>

          {isAdmin && !autoLogin && (
            <HeaderMenuItemButton
              onClick={() => {
                navigate("/admin");
              }}
            >
              <span
                data-testid="menu_admin_page_button"
                id="menu_admin_page_button"
              >
                管理员面板
              </span>
            </HeaderMenuItemButton>
          )}

          <div className="flex items-center justify-between px-4 py-[6.5px]">
            <div className="text-sm">主题</div>
            <div>
              <ThemeButtons />
            </div>
          </div>

          {!autoLogin && (
            <HeaderMenuItemButton onClick={handleLogout} icon="log-out">
              登出
            </HeaderMenuItemButton>
          )}
        </HeaderMenuItems>
      </HeaderMenu>
    </>
  );
};
