import styles from "@/styles/header/Header.module.css";
import animations from "@/styles/header/Animation.module.css";
import Image from "next/image";
import { useEffect, useRef, useState } from "react";

interface headerProps {
  environment: 'pc' | 'mobile'
  categories: Array<string>
  contents: Array<string>
  selectedCategory: string
  changeMarkDownFile: Function
  scrollToContent: Function
}

const hamburgerIcon = {
  src: require('@/public/icons/hamburger.svg'),
  alt: 'hamburgerIcon'
}

const arrowIcon = {
  src: require('@/public/icons/arrow.svg'),
  alt: 'arrowIcon'
}

const header = (props: headerProps) => {
  const sidebarContentContainerRef = useRef<HTMLDivElement>(null);

  const [toggledSidebar, setToggledSidebar] = useState<boolean>(false);
  const [closeSidebarTrigger, setCloseSidebarTrigger] = useState<boolean>(false);

  const [toggledContents, setToggledContents] = useState<boolean>(false);

  const toggleSidebar = (wait?: 'wait') => {
    if (wait) {
      setCloseSidebarTrigger(true);
      setTimeout(() => {
        setToggledSidebar(!toggledSidebar);
      }, 300);
    }
    else {
      setCloseSidebarTrigger(false);
      setToggledSidebar(!toggledSidebar);
    }
  }

  const changeMarkDownFile = (index: number) => {
    setToggledContents(false);
    toggleSidebar('wait');
    props.changeMarkDownFile(index);
  }

  const scrollToContent = (index: number) => {
    toggleSidebar('wait');
    props.scrollToContent(index);
  }

  useEffect(() => {
    if (toggledSidebar) document.body.setAttribute('style', 'overflow: hidden; touch-action: none;');
    else document.body.setAttribute('style', 'overflow: auto');

  }, [toggledSidebar]);
  
  useEffect(() => {
    if (!toggledContents && closeSidebarTrigger) document.documentElement.style.setProperty('--sidebar-content-container-height', `0px`);
    else if (toggledContents) document.documentElement.style.setProperty('--sidebar-content-container-height', `${sidebarContentContainerRef.current?.clientHeight}px`);
  }, [toggledContents, closeSidebarTrigger]);

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
          {
            props.categories.map((category, index) =>
              category === props.selectedCategory ? (
                <div key={index}>
                  <div className={`${styles.sidebarCategoryBackground}`}>
                    <div className={`${styles.sidebarCategoryContainer}`} onClick={() => setToggledContents(!toggledContents)}>
                      <Image className={`${styles.arrowIcon} ${toggledContents && styles.toggledArrowIcon}`} src={arrowIcon.src} alt={arrowIcon.alt} />
                      <h1 className={`${styles.sidebarCategory} ${category === props.selectedCategory && styles.selectedSidebarCategory}`}>{ category }</h1>
                    </div>
                  </div>
                  <div className={`${styles.sidebarContentBackground} ${toggledContents ? animations.sidebarContentBackgroundIncrease : animations.sidebarContentBackgroundDecrease}`}>
                    <div className={`${styles.sidebarContentContainer} ${toggledContents && styles.toggledSidebarContentContainer}`} ref={sidebarContentContainerRef}>
                      {
                        props.contents.map((content, index) =>
                          <div className={`flex`}>
                            <p className={`${styles.sidebarContent}`} onClick={() => scrollToContent(index)} key={index}>{ content }</p>
                          </div>
                        )
                      }
                    </div>
                  </div>
                </div>
              ) : (
                <div className={`flex`}>
                  <h1 className={`${styles.sidebarCategory} ${category === props.selectedCategory && styles.selectedSidebarCategory}`} onClick={() => changeMarkDownFile(index)} key={index}>{ category }</h1>
                </div>
              )
            )
          }
        </div>
        <div className={`${styles.sidebarWhiteSpace} ${closeSidebarTrigger ? animations.sidebarWhiteSpaceFadeOut : animations.sidebarWhiteSpaceFadeIn}`} onClick={() => toggleSidebar('wait')} />
      </div> }
    </>
  );
}

export default header;