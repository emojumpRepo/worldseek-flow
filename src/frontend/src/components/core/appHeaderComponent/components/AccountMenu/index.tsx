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
          {ENABLE_DATASTAX_LANGFLOW && (
            <HeaderMenuItemsSection>
              <CustomHeaderMenuItemsTitle />
            </HeaderMenuItemsSection>
          )}
          <HeaderMenuItemsSection>
            <div className="flex h-[46px] w-full items-center justify-between px-3">
              <div className="pl-1 text-xs text-zinc-500">
                <span
                  data-testid="menu_version_button"
                  id="menu_version_button"
                >
                  Theme
                </span>
              </div>
            </div>

            <div>
              <HeaderMenuItemButton
                onClick={() => {
                  navigate("/settings");
                }}
              >
                <span
                  data-testid="menu_settings_button"
                  id="menu_settings_button"
                >
                  Settings
                </span>
              </HeaderMenuItemButton>

              {isAdmin && !autoLogin && (
                <div>
                  <HeaderMenuItemButton
                    onClick={() => {
                      navigate("/admin");
                    }}
                  >
                    <span
                      data-testid="menu_admin_page_button"
                      id="menu_admin_page_button"
                    >
                      Admin Page
                    </span>
                  </HeaderMenuItemButton>
                )}
              </>
            )}
          </HeaderMenuItemsSection>
          {ENABLE_DATASTAX_LANGFLOW ? (
            <HeaderMenuItemsSection>
              <HeaderMenuItemLink href="/session/logout" icon="log-out">
                Logout
              </HeaderMenuItemLink>
            </div>

            <div className="flex items-center justify-between px-4 py-[6.5px] text-sm">
              <span className="">Theme</span>
              <div className="relative top-[1px] float-right">
                <ThemeButtons />
              </div>
            </div>

            {!autoLogin && (
              <div>
                <HeaderMenuItemButton onClick={handleLogout} icon="log-out">
                  Logout
                </HeaderMenuItemButton>
              </div>
            )}
          </div>
        </HeaderMenuItems>
      </HeaderMenu>
    </>
  );
};
