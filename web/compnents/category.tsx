import styles from "@/styles/category/Category.module.css";
import { useEffect, useState } from "react";

interface categoryProps {
  title: 'ArtificialVision' | 'Table of contents'
  categories?: Array<string>
  selectedCategory?: string
  contents?: Array<string>
  subContents?: Array<string>
  onClick?: Function
}

const category = (props: categoryProps) => {
  const [listContainerHeight, setListContainerHeight] = useState<number>(0);

  let timeoutId: NodeJS.Timeout;
  const resizeListContainerHeight = () => {
    clearInterval(timeoutId);
    timeoutId = setTimeout(() => setListContainerHeight(window.innerHeight - 180), 100);
  }

  useEffect(() => {
    window.addEventListener('resize', resizeListContainerHeight);
    resizeListContainerHeight();
  }, []);

  return (
    <div className={`${styles.categoryBackground}`}>
      <div className={`${styles.categoryContainer}`}>
        <div className={`${styles.titleContainer}`}>
          <h1 className={`${styles.titleText}`}>{ props.title }</h1>
        </div>
        <div className={`${styles.listContainer}`} style={{height: listContainerHeight}}>
          {
            props.title === 'ArtificialVision' ? (
              props.categories?.map((content, index) => (
                <div className={`${styles.contentContainer}`} onClick={() => props.onClick && props.onClick(index)} key={index}>
                  <p className={`${styles.contentText} ${props.selectedCategory === content && styles.selectedContentText}`}>{ content }</p>
                </div>
              ))
            ) : (
              props.contents?.map((content, index) => (
                <div className={`${styles.contentContainer}`} onClick={() => props.onClick && props.onClick(index)} key={index}>
                  <p className={`${styles.contentText}`}>{ content }</p>
                </div>
              ))
            )
          }
        </div>
      </div>
    </div>
  );
}

export default category;