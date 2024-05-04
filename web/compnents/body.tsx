import styles from "@/styles/body/Body.module.css";
import { ReactNode } from "react";

interface bodyProps {
  children: ReactNode
}

const body = (props: bodyProps) => {
  return (
    <div className={`${styles.bodyBackground}`}>
      <div className={`${styles.bodyContainer}`}>
        { props.children }
      </div>
    </div>
  );
}

export default body;