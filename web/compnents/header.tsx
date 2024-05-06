import styles from "@/styles/header/Header.module.css";
import animations from "@/styles/header/animation.module.css"
import Image from "next/image";
import { useState } from "react";

interface headerProps {
  environment: 'pc' | 'mobile'
}

const hamburgerIcon = {
  src: require('@/public/icons/hamburger.svg'),
  alt: 'hamburgerIcon'
}

const header = (props: headerProps) => {
  const [toggledSidebar, setToggledSidebar] = useState<boolean>(false);
  const [closeSidebarTrigger, setCloseSidebarTrigger] = useState<boolean>(false);

  const toggleSidebar = (wait?: 'wait') => {
    if (wait) {
      setCloseSidebarTrigger(true);
      setTimeout(() => setToggledSidebar(!toggledSidebar), 300);
    }
    else {
      setCloseSidebarTrigger(false);
      setToggledSidebar(!toggledSidebar);
    }
  }

  return (
    <>
      <div className={`${styles.headerBackground}`}>
        <div className={`${styles.headerContainer}`}>
          {
            props.environment === 'mobile' && (
              <div className={`${styles.hamburgerContainer}`} onClick={() => toggleSidebar()}>
                <Image className={`${styles.hamburgerIcon}`} src={hamburgerIcon.src} alt={hamburgerIcon.alt} />
              </div>
            )
          }
          <div className={`${styles.titleContainer}`}>
            <h1 className={`${styles.titleText}`}>Atrificial</h1>
            <h1 className={`${styles.titleText}`}>Vision</h1>
          </div>
          <div className={`${styles.searchContainer}`}>
            <input className={`${styles.searchInput}`} type="text" placeholder="Search" />
          </div>
          <div className={`${styles.sourceContainer}`}>
          </div>
        </div>
      </div>
      { toggledSidebar && <div className={`${styles.sidebarBackground}`}>
        <div className={`${styles.sidebarContainer} ${closeSidebarTrigger ? animations.sidebarSlideOut : animations.sidebarSlideIn}`}>

        </div>
        <div className={`${styles.sidebarWhiteSpace} ${closeSidebarTrigger ? animations.sidebarWhiteSpaceFadeOut : animations.sidebarWhiteSpaceFadeIn}`} onClick={() => toggleSidebar('wait')} />
      </div> }
    </>
  );
}

export default header;