import styles from "@/styles/header/Header.module.css";

const header = () => {
  return (
    <div className={`${styles.headerBackground}`}>
      <div className={`${styles.headerContainer}`}>
        <div className={`${styles.titleContainer}`}>
          <h1 className={`${styles.titleText}`}>ArtificialVision</h1>
        </div>
        <div className={`${styles.searchContainer}`}>
          <input className={`${styles.searchInput}`} type="text" placeholder="Search" />
        </div>
        <div className={`${styles.sourceContainer}`}>
        </div>
      </div>
    </div>
  );
}

export default header;