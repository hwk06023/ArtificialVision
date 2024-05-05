import { Body, Category, Header } from "@/compnents/index";
import styles from "@/styles/Home.module.css";
import fs from "fs";
import path from "path";
import matter from "gray-matter";
import { remark } from "remark";
import remarkGfm from "remark-gfm";
import html from "remark-html";
import { GetServerSideProps, InferGetServerSidePropsType } from "next";
import { useEffect, useState } from "react";
import { useRouter } from "next/router";

const home = (serverSideProps: InferGetServerSidePropsType<typeof getServerSideProps>) => {
  const router = useRouter();

  const [environment, setEnvironment] = useState<'pc' | 'mobile'>('pc');

  const [markDownHtml, setMarkDownHtml] = useState<string>('');

  const [contents, setContents] = useState<Array<HTMLHeadingElement>>([]);
  const [contentNames, setContentNames] = useState<Array<string>>([]);

  const markDownFiles: Array<string> = serverSideProps.markDownFiles;

  const changeMarkDownFile = (index: number) => {
    router.push(`?page=${markDownFiles[index]}`, undefined, { shallow: false });
  }

  const scrollToContent = (index: number) => {
    const headerOffset = 80;
    const contentPosition = contents[index].getBoundingClientRect().top;
    const offsetPosition = contentPosition + window.scrollY - headerOffset;

    window.scrollTo({ top: offsetPosition });
  }

  let timeoutId: NodeJS.Timeout;
  const checkEnvironment = () => {
    clearInterval(timeoutId);
    timeoutId = setTimeout(() => {
      if (window.innerWidth > 1024) setEnvironment('pc');
      else setEnvironment('mobile');
    }, 100);
  }

  useEffect(() => {
    let html = serverSideProps.content;
    html = html.replace(/<hr>/g, '');
    html = html.replace(/<img id="logo"/g, `<img class="${styles.markDownImage}"`);
    html = html.replace(/<h1>/g, `<h1 class="${styles.markDownTitleText}">`);
    html = html.replace(/<h2>/g, `<h2 class="${styles.markDownContentText}">`);
    html = html.replace(/<h3>/g, `<h3 class="${styles.markDownSubContentText}">`);
    html = html.replace(/<p>/g, `<p class="${styles.markDownNormalText}">`);
    html = html.replace(/<pre>/g, `<pre class="${styles.markDownPre}">`);
    html = html.replace(/<code/g, `<code class="${styles.markDownCode}"`);
    html = html.replace(/<ul>/g, `<ul class="${styles.markDownUl}">`);
    html = html.replace(/<li>/g, `<li class="${styles.markDownLi}">`);
    html = html.replace(/<table>/g, `<table class="${styles.markDownTable}">`);
    // html = html.replace(/<table>/g, ``);

    setMarkDownHtml(html);
  }, [serverSideProps.page]);

  useEffect(() => {
    if (markDownHtml) {
      let contents: Array<HTMLHeadingElement> = [];
      let contentNames: Array<string> = [];
      document.querySelectorAll('h2').forEach((element) => {
        contents.push(element);
        contentNames.push(element.outerText);
      });

      setContents(contents);
      setContentNames(contentNames);
    }
  }, [markDownHtml]);

  useEffect(() => {
    window.addEventListener('resize', checkEnvironment);
    checkEnvironment();
  }, []);

  return (
    <>
      <Header />
      <Body>
        { environment === 'pc' && <Category title="ArtificialVision" categories={markDownFiles} selectedCategory={serverSideProps.page} onClick={changeMarkDownFile} /> }
        <div className={`${styles.markDown}`} dangerouslySetInnerHTML={{ __html: markDownHtml }} />
        { environment === 'pc' && <Category title="Table of contents" contents={contentNames} onClick={scrollToContent} /> }
      </Body>
    </>
  );
}

export const getServerSideProps: GetServerSideProps = async (context) => {
  const root = './public/markDown/';

  const markDownDirectory = path.join(process.cwd(), root);
  const files = fs.readdirSync(markDownDirectory);

  let markDownFiles: Array<string> = [];
  files.map((file) => {
    if (file.includes('.md')) markDownFiles.push(file.replace(/\.md$/, ''));
  });

  const page = context.query.page || 'Read';
  const markDownFilePath = path.join(process.cwd(), `${root}${page}.md`);
  const fileContents = fs.readFileSync(markDownFilePath, 'utf8');
  const { content } = matter(fileContents);

  const processedContent = await remark()
    .use(remarkGfm)
    .use(html, { sanitize: false })
    .process(content);

  const htmlContent = processedContent.toString();

  return {
    props: {
      markDownFiles: markDownFiles.reverse(),
      content: htmlContent,
      page: page
    }
  }
}

export default home;