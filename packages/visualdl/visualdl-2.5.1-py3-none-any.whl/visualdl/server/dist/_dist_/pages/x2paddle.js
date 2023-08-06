import a,{useState as d,useEffect as z,useRef as v,useCallback as C,useMemo as I}from"../../__snowpack__/pkg/react.js";import{rem as m,primaryColor as N,size as q}from"../utils/style.js";import H from"../components/Content.js";import{toast as i}from"../../__snowpack__/pkg/react-toastify.js";import{fetcher as j}from"../utils/fetch.js";import M from"./graphStatic3.js";import Y from"./graphStatic2.js";import P from"../../__snowpack__/pkg/react-spinners/HashLoader.js";import h from"../../__snowpack__/pkg/styled-components.js";import{useTranslation as X}from"../../__snowpack__/pkg/react-i18next.js";const J=h.section`
    display: flex;
    .active {
        background-color: #2932e1;
        color: white;
    }
    .un_active {
        background-color: white;
        color: #2932e1;
    }
    .disabled {
        background: #ccc;
        color: white;
        cursor: not-allowed;
    }
`,K=h.article`
    flex: auto;
    display: flex;
    min-width: 0;
    margin: ${10};
    min-height: ${10};
`,w=h.div`
    width: 49%;
    height: ${m(40)};
    line-height: ${m(40)};
    text-align: center;
    font-size: 16px;
`,Q=h.div`
    height: 100%;
`,V=h.div`
    ${q("100%","100%")}
    display: flex;
    flex-direction: column;
    justify-content: center;
    align-items: center;
    overscroll-behavior: none;
    cursor: progress;
    font-size: ${m(16)};
    line-height: ${m(60)};
`,W=h.aside`
    width: ${m(260)};
    display: flex;
`;function Z(){const{t:r}=X(["togglegraph"]),[l,_]=d({show:!0,show2:!1}),[s,k]=d(null),[$,A]=d(!1),[y,c]=d(!1),[F,R]=d(!1),[f,S]=d(""),p=v(null),b=v(null),x=v(null),G=(t,n)=>{const e=atob(t);let o=e.length;const g=new Uint8Array(o);for(;o--;)g[o]=e.charCodeAt(o);return new File([g],n)},L=(t,n="\u672A\u77E5\u6587\u4EF6")=>{const e=document.createElement("a");e.style.display="none",e.setAttribute("target","_blank"),n&&e.setAttribute("download",n);const o=URL.createObjectURL(t);e.href=o,console.log(e,o),document.body.appendChild(e),e.click(),document.body.removeChild(e)},u=(t,n="caffe")=>{if(!t){i.warning("\u8BF7\u4E0A\u4F20\u6A21\u578B\u6587\u4EF6\u6A21\u578B\u6587\u4EF6");return}c(!0);const e=new FormData;e.append("file",t[0]),e.append("filename",t[0].name),e.append("format",n),j(`/inference/convert?format=${n}`,{method:"POST",body:e}).then(o=>{const g=t[0].name.substring(t[0].name.lastIndexOf(".")+1)+".paddle";console.log("res",o,g);const E=G(o.pdmodel,g);console.log("file",E),k(E),A(o.request_id);const U=t[0].name.substring(0,t[0].name.lastIndexOf("."));R(U+".tar"),c(!1)},o=>{console.log("errres",o),c(!1)})},T=C(()=>{var o;if(s){i.warning(r("warin-info6"));return}console.log("Graph.current.filess",b);const t=b,n=(o=t==null?void 0:t.current)==null?void 0:o.files,e=n[0].name.substring(n[0].name.lastIndexOf(".")+1);if(e==="prototxt"){i.warning(r("togglegraph:warin-info")),p.current&&(p.current.value="",p.current.click());return}if(e==="pb"||e==="onnx"){u(n,e);return}i.warning(r("togglegraph:warin-info2"))},[u,s,r]),B=C(t=>{const n=t.target;n&&n.files&&n.files.length&&u(n.files)},[u]),D=(t,n)=>{console.log("baseId",t,n),!(t===void 0||!n)&&(c(!0),j(`/inference/download?request_id=${t}`,{method:"GET"}).then(e=>{console.log("blobres",e,e.data),L(e.data,n),c(!1)},e=>{console.log("errres",e),c(!1)}))};z(()=>{var n;const t=x;if(s){console.log("Graph2",s);const e=[s];(n=t==null?void 0:t.current)==null||n.setModelFiles(e)}},[s]);const O=I(()=>a.createElement("div",{style:{height:l.show2?"auto":"0px",overflowY:"hidden"}},a.createElement(Y,{ref:x,changeRendered:()=>{_({show:!1,show2:!0})},show:l.show2})),[l.show2]);return console.log("show",l),a.createElement(H,null,y&&a.createElement(V,null,a.createElement(P,{size:"60px",color:N})),a.createElement(Q,{style:{height:y?"0px":"auto",overflow:"hidden"}},a.createElement("div",{style:{height:l.show?"auto":"0px",overflowY:"hidden"}},a.createElement(M,{ref:b,changeName:S,show:l.show,changeshowdata:()=>{k(null)},Xpaddlae:!0})),O),f&&!y&&a.createElement(J,{style:{marginTop:"20px"}},a.createElement(K,null,a.createElement(w,{style:{marginRight:"3px"},className:l.show?"active":"un_active",onClick:()=>{_({show:!0,show2:!1})}},f||"Toggle"),a.createElement(w,{className:s?l.show2?"active":"un_active":"disabled",onClick:()=>{if(!s){i.warning(r("warin-info3"));return}_({show:!1,show2:!0})}},"paddle")),a.createElement(W,null,a.createElement(w,{style:{marginRight:"3px"},className:!s&&f?"active":"disabled",onClick:()=>{if(s){i.warning(r("warin-info4"));return}else f?T():i.warning(r("warin-info7"))}},r("togglegraph:transformation")),a.createElement(w,{className:s?"active":"disabled",onClick:()=>{if(console.log("showData",s),!s){i.warning(r("warin-info5"));return}D($,F)}},r("togglegraph:download")))),a.createElement("input",{ref:p,type:"file",multiple:!1,onChange:B,style:{display:"none"}}))}export default Z;
