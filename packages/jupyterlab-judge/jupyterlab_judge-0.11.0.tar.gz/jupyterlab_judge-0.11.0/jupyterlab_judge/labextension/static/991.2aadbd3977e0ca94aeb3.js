"use strict";(self.webpackChunkjupyterlab_judge=self.webpackChunkjupyterlab_judge||[]).push([[991],{4991:(e,t,n)=>{n.r(t),n.d(t,{IJudgePanelFactoryRegistry:()=>he,IJudgeSignal:()=>ge,IProblemProviderRegistry:()=>me,default:()=>fe,openOrCreateFromId:()=>re});var s=n(6866),o=n(5510),i=n(5442),r=n(6591),a=n(3606),l=n(4379),d=n(841),u=n(7346),c=n(420),m=n(6271),h=n.n(m);const g="jupyterlab-judge",p="judgedrive",b=".jce-judge",_="jupyterlab-judge";var C;!function(e){function t(e,t){const n=t.load(g);function s(){if(e.context.model.readOnly)return(0,o.showDialog)({title:n.__("Cannot Save"),body:n.__("Document is read-only"),buttons:[o.Dialog.okButton({label:n.__("Ok")})]});e.context.save().then((()=>{if(!e.isDisposed)return e.context.createCheckpoint()}))}return(0,o.addToolbarButtonClass)(o.ReactWidget.create(m.createElement(o.UseSignal,{signal:e.context.fileChanged},(()=>m.createElement(o.ToolbarButtonComponent,{icon:r.saveIcon,onClick:s,tooltip:n.__("Save the judge contents and create checkpoint"),enabled:!!(e&&e.context&&e.context.contentsModel&&e.context.contentsModel.writable)})))))}e.createSaveButton=t,e.getDefaultItems=function(e,n,s){return[{name:"save",widget:t(e,n)}]}}(C||(C={}));var y=n(1431);const w="jp-OutputArea-output";class x extends c.OutputArea{constructor(e){super(e),this.addClass("jp-JudgeOutputArea");const t=e.translator.load(g),n=document.createElement("div");n.className="jp-JudgeOutputArea-placeholder",n.textContent=t.__("Execution result will be shown here"),this.node.appendChild(n)}createOutputItem(e){const t=this.createRenderedMimetype(e);return t&&t.addClass(w),t}onInputRequest(e,t){const n=this.contentFactory,s=e.content.prompt,o=e.content.password,i=new y.Panel;i.addClass("jp-OutputArea-child"),i.addClass("jp-OutputArea-stdin-item");const r=n.createStdin({prompt:s,password:o,future:t});r.addClass(w),i.addWidget(r),this.layout.addWidget(i),r.value.then((e=>{this.model.add({output_type:"stream",name:"stdin",text:e+"\n"}),i.dispose()}))}}class f extends y.Panel{constructor(e){super(),this.addClass("jp-JudgeTerminal");const t=e.translator.load(g),n=new y.Widget;n.addClass("jp-JudgeTerminal-toolbar");const s=document.createElement("button");s.className="jp-JudgeTerminal-executeButton",r.runIcon.element({container:s});const o=document.createElement("span");o.className="jp-JudgeTerminal-executeButtonLabel",o.textContent=t.__("Execute"),s.addEventListener("click",(async()=>{s.disabled=!0,await e.panel.execute(),s.disabled=!1})),s.appendChild(o);const i=document.createElement("div");i.className="jp-JudgeTerminal-seperator";const a=document.createElement("button");a.className="jp-JudgeTerminal-stopButton",r.stopIcon.element({container:a});const l=document.createElement("span");l.className="jp-JudgeTerminal-stopButtonLabel",l.textContent=t.__("Stop"),a.addEventListener("click",(()=>{e.panel.session.shutdown()})),a.appendChild(l),n.node.appendChild(s),n.node.appendChild(i),n.node.appendChild(a),this.addWidget(n),this._outputArea=new x(e),this.addWidget(this._outputArea)}get outputArea(){return this._outputArea}}var v=n(3848),S=n(8149),I=n.n(S);const P=I().div`
  background: var(--jp-layout-color2);
`,j=I().button`
  display: block;
  margin-top: 12px;
  margin-left: 20px;
  margin-right: 20px;
  padding: 11px 17px;

  cursor: pointer;

  border: none;

  background: var(--jp-brand-color1);

  /* Shadow-2 */
  box-shadow: 0px 0.15px 0.45px rgba(0, 0, 0, 0.11),
    0px 0.8px 1.8px rgba(0, 0, 0, 0.13);
  border-radius: 8px;

  font-family: 'Noto Sans KR';
  font-style: normal;
  font-weight: 700;
  font-size: 16px;
  line-height: 22px;
  /* identical to box height, or 138% */

  color: var(--jp-ui-inverse-font-color0);

  :disabled {
    background: var(--jp-layout-color3);
    cursor: not-allowed;
  }

  :hover {
    background: var(--jp-brand-color0);
  }
`;var E=n(4886);const k=I().span``,N=I().li`
  display: flex;
  padding: 5px 12px;
  height: 16px;

  font-family: 'Noto Sans KR';
  font-style: normal;
  font-size: 12px;
  line-height: 16px;
`,M=I()((function(e){const t=(0,m.useContext)(Q);let n="",s="";switch(e.status){case"AC":n=`👍 ${t.__("Accepted")}`;break;case"WA":n=`❌ ${t.__("Wrong")}`,s=`(${e.acceptedCount}/${e.totalCount})`;break;case"RE":n=`🚫 ${t.__("Error")}`;break;case"TLE":n=`🕓 ${t.__("Time Limit")}`;break;case"OLE":n=`👀 ${t.__("Output Limit")}`;break;case"IE":n=`☠ ${t.__("Please Try Again")}`}return h().createElement(k,{className:e.className,title:s},n)}))`
  height: 16px;
  flex-grow: 0;
  flex-shrink: 0;

  width: 101px;
  margin-right: 8px;
`,T=I().button`
  height: 16px;
  flex-grow: 0;
  flex-shrink: 0;

  all: unset;
  cursor: pointer;

  font-family: 'Noto Sans KR';
  font-style: normal;
  font-weight: 700;
  font-size: 12px;
  line-height: 16px;
  color: var(--jp-brand-color1);
`,O=I().span`
  height: 16px;
  flex-grow: 1;
  flex-shrink: 1;

  text-align: right;

  font-family: 'Noto Sans KR';
  font-style: normal;
  font-weight: 400;
  font-size: 12px;
  line-height: 16px;

  color: var(--jp-ui-font-color3);
`,A=I().span``,F=I().li`
  display: flex;
  padding: 5px 12px;
  height: 16px;

  font-family: 'Noto Sans KR';
  font-style: normal;
  font-size: 12px;
  line-height: 16px;
`,J=I()((function(e){const{status:t}=e,n=(0,m.useContext)(Q);return t.inProgress?h().createElement(A,{className:e.className},`⌛ ${n.__("In Progress")} (${t.runCount}/${t.totalCount})`):h().createElement(h().Fragment,null)}))`
  height: 16px;
  flex-grow: 0;
  flex-shrink: 0;

  width: 101px;
  margin-right: 8px;
`;function R(e){const t=(0,m.useContext)(Q);if(null===e.problemId)return h().createElement(L,{className:e.className},"⌛ ",t.__("Loading History"));const{data:n,isLoading:s}=(0,v.useQuery)(["submissions",e.problemId],e.getSubmissions);if(s)return h().createElement(L,{className:e.className},"⌛ ",t.__("Loading History"));if(void 0===n)return h().createElement(L,{className:e.className},"🚫 ",t.__("History Not Available"));const o=e.submissionStatus&&e.submissionStatus.inProgress;return 0!==n.length||o?h().createElement($,{className:e.className},e.submissionStatus&&e.submissionStatus.inProgress&&h().createElement(W,{status:e.submissionStatus}),n.map((t=>h().createElement(D,{submission:t,key:t.id,setCode:e.setCode})))):h().createElement(B,{className:e.className},t.__("Submit your code to get results here."))}const $=I().ul`
  padding: 7px 0px 0px 0px;
  margin: 0px;

  overflow-y: auto;

  /* width */
  ::-webkit-scrollbar {
    width: 2px;
  }

  /* Handle */
  ::-webkit-scrollbar-thumb {
    background: var(--jp-border-color0);
    border-radius: 12px;
  }
`,D=I()((function(e){const t=(0,m.useContext)(Q);let n=E.Time.formatHuman(new Date(e.submission.createdAt)),s=E.Time.format(new Date(e.submission.createdAt),"lll");return h().createElement(N,{className:e.className},h().createElement(M,{status:e.submission.status,acceptedCount:e.submission.acceptedCount,totalCount:e.submission.totalCount}),h().createElement(T,{onClick:()=>{e.setCode(e.submission.code)},title:e.submission.code.substring(0,1e3)},t.__("Load this submission")),h().createElement(O,{title:s},n))}))``,W=I()((function(e){return h().createElement(F,{className:e.className},h().createElement(J,{status:e.status}))}))``,L=I().div`
  text-align: center;
  padding: 5px;
  font-size: var(--jp-ui-font-size2);
`,B=I().div`
  padding: 12px;
  font-weight: 700;
  font-size: 12px;
  line-height: 16px;
  color: var(--jp-ui-font-color3);
`;function K(e){const t=(0,m.useContext)(Q);return null===e.model?h().createElement("div",null,t.__("No Submission History Found.")):h().createElement(z,null,h().createElement(q,{model:e.model}),h().createElement(H,{panel:e.panel}))}const z=I().div`
  display: flex;
  border-top: 4px solid var(--jp-border-color0);
  font-size: var(--jp-ui-font-size1);

  height: 100%;
`,q=I()((function(e){const t=(0,v.useQueryClient)();return h().createElement(o.UseSignal,{signal:e.model.problemChanged,initialSender:e.model,initialArgs:e.model.problem},((n,s)=>h().createElement(o.UseSignal,{signal:e.model.submissionsChanged,initialSender:e.model},((n,i)=>{var r;const a=null!==(r=null==s?void 0:s.id)&&void 0!==r?r:null;return a&&t.invalidateQueries(["submissions",a]),h().createElement(o.UseSignal,{signal:e.model.submissionStatusChanged,initialSender:e.model,initialArgs:e.model.submissionStatus},((t,n)=>h().createElement(R,{className:e.className,problemId:a,getSubmissions:async()=>{const t=await e.model.submissions();return null!=t?t:[]},setCode:t=>{e.model.source=t},submissionStatus:null!=n?n:null})))}))))}))`
  flex-grow: 1;
  flex-shrink: 1;

  margin-right: 2px;
`,H=I()((function(e){const t=(0,m.useContext)(Q),[n,s]=(0,m.useState)(!1);return h().createElement(P,{className:e.className},h().createElement(j,{onClick:async()=>{s(!0),await e.panel.judge(),s(!1)},disabled:n},t.__("Submit")))}))`
  flex-grow: 0;
  flex-shrink: 0;
`,Q=h().createContext(i.nullTranslator.load(g));class U extends o.ReactWidget{constructor(e){super(),this.queryClient=new v.QueryClient,this._panel=e.panel,this._model=e.model,this._translator=e.translator}render(){var e,t;return h().createElement(Q.Provider,{value:this._translator.load(g)},h().createElement(v.QueryClientProvider,{client:this.queryClient},h().createElement(K,{key:null!==(t=null===(e=this._model.problem)||void 0===e?void 0:e.id)&&void 0!==t?t:"",panel:this._panel,model:this._model})))}}class Y extends y.BoxPanel{constructor(e){super(),this.addClass("jp-JudgePanel"),this._context=e.context,this._translator=e.translator,this._trans=this._translator.load(g),this._submitted=e.submitted,this.id="jce-judge-panel",this.title.closable=!0;const t=new y.SplitPanel({spacing:0});t.addClass("jp-JudgePanel-splitPanel"),this._editorWidget=new a.CodeEditorWrapper({model:this.model.codeModel,factory:(new u.CodeMirrorEditorFactory).newInlineEditor,config:Object.assign(Object.assign({},e.editorConfig),{lineNumbers:!0})}),this._editorWidget.addClass("jp-JudgePanel-editor"),this._markdownRenderer=e.rendermime.createRenderer("text/markdown"),this._markdownRenderer.addClass("jp-JudgePanel-markdown"),this.renderProblem(),this.model.problemChanged.connect(((e,t)=>{this.renderProblem(),(null==t?void 0:t.title)&&(this.title.label=`${null==t?void 0:t.title}.judge`)})),this._terminal=new f({panel:this,model:this.model.outputAreaModel,rendermime:e.rendermime,translator:this._translator}),this._terminal.addClass("jp-JudgePanel-terminal");const n=new U({panel:this,model:this.model,translator:this._translator});n.addClass("jp-JudgePanel-submissionPanel"),t.addWidget(this._markdownRenderer);const s=new y.SplitPanel({orientation:"vertical",spacing:0});s.addClass("jp-JudgePanel-rightPanel"),s.addWidget(this._editorWidget),s.addWidget(this._terminal),s.addWidget(n),t.addWidget(s),this.addWidget(t),this.session.isReady||this.session.initialize()}get model(){return this.context.model}get editor(){return this._editorWidget.editor}get session(){return this.context.sessionContext}get context(){return this._context}renderProblem(){var e,t;this._markdownRenderer.renderModel(new d.MimeModel({data:{"text/markdown":null!==(t=null===(e=this.model.problem)||void 0===e?void 0:e.content)&&void 0!==t?t:this._trans.__("Problem Not Available.")}}))}handleEvent(e){this.model&&"mousedown"===e.type&&this._ensureFocus()}onAfterAttach(e){super.onAfterAttach(e),this.node.addEventListener("mousedown",this)}onBeforeDetach(e){this.node.removeEventListener("mousedown",this)}onActivateRequest(e){this._ensureFocus()}_ensureFocus(){this.session.pendingInput||this.editor.hasFocus()||this.editor.focus()}async execute(){if(this.session.hasNoKernel)return o.sessionContextDialogs.selectKernel(this.session),null;if(this.session.pendingInput)return(0,o.showDialog)({title:this._trans.__("Cell not executed due to pending input"),body:this._trans.__("The cell has not been executed to avoid kernel deadlock as there is another pending input! Submit your pending input and try again."),buttons:[o.Dialog.okButton({label:this._trans.__("Ok")})]}),null;const e=this.model.source,t=await c.OutputArea.execute(e,this._terminal.outputArea,this.session,{});return await this.session.restartKernel(),t||null}async judge(){var e,t;const n=this.model.problem;if(null===n)throw new Error("Problem cannot be found.");const s=null===(e=this.session.session)||void 0===e?void 0:e.kernel;if(!s)return void o.sessionContextDialogs.selectKernel(this.session);const i=new o.SessionContext({sessionManager:this.session.sessionManager,specsManager:this.session.specsManager,name:"Judge"});await i.initialize(),await i.changeKernel(await s.spec);const r=null===(t=i.session)||void 0===t?void 0:t.kernel;if(!r)return void o.sessionContextDialogs.selectKernel(i);const a=await this.model.getTestCases(),l=[];this.model.submissionStatus={inProgress:!0,runCount:0,totalCount:a.length};for(let e of a){const t=await this.runWithInput(r,n,e);l.push(t),this.model.submissionStatus={inProgress:!0,runCount:l.length,totalCount:a.length}}let d=null;const u=await this.model.validate(l.map((e=>e.output)));d=u.acceptedCount===u.totalCount?"AC":l.some((e=>"RE"==e.status))?"RE":l.some((e=>"OLE"==e.status))?"OLE":l.some((e=>"TLE"==e.status))?"TLE":"WA",await r.shutdown(),r.dispose();const c=await this.model.submit({problemId:n.id,status:d,code:this.model.source,cpuTime:l.map((e=>e.cpuTime)).reduce(((e,t)=>e+t),0)/l.length,acceptedCount:u.acceptedCount,totalCount:u.totalCount,token:u.token,language:"python",memory:0});this.model.submissionStatus={inProgress:!1,runCount:0,totalCount:0},this._submitted.emit({widget:this,submission:c,problem:n})}async runWithInput(e,t,n,s=!1){const o={code:this.model.source,stop_on_error:!0,allow_stdin:!0};s&&await e.restart();const i=new Promise(((t,n)=>{const s=(n,o)=>{"idle"===o&&(e.statusChanged.disconnect(s),t())};"idle"===e.status?t():e.statusChanged.connect(s)}));await i;let r=[];r="one_line"===t.inputTransferType?n.split(/\r?\n/):[n];const a=Date.now(),l=e.requestExecute(o,!0,{});l.onStdin=e=>{if("input_request"==e.header.msg_type){const t=r.shift();l.sendInputReply({value:null!=t?t:"",status:"ok"},e.header)}};let d={output:"",status:"OK",cpuTime:0};l.onIOPub=e=>{switch(e.header.msg_type){case"stream":const t=e;"stdout"===t.content.name&&(d.output=d.output.concat(t.content.text));break;case"error":d.status="RE"}};const u=1e3*t.timeout,c=new Promise((e=>{setTimeout((()=>{e(0)}),1.2*u)}));if(0===await Promise.race([l.done,c]))l.dispose(),await e.interrupt(),d.status="TLE";else{const e=Date.now()-a;e>u?d.status="TLE":d.cpuTime=e}return d}}class G extends l.DocumentWidget{constructor(e){super(e),C.getDefaultItems(this.content,e.translator).forEach((e=>{this.toolbar.addItem(e.name,e.widget)}))}}class V extends l.ABCWidgetFactory{constructor(e){super(e.factoryOptions),this._rendermime=e.rendermime,this._commands=e.commands,this._editorConfig=e.editorConfig,this._judgePanelFactory=e.judgePanelFactory,this._submitted=e.submitted}createNewWidget(e){const t=this._judgePanelFactory({rendermime:this._rendermime,editorConfig:this._editorConfig,context:e,translator:this.translator,submitted:this._submitted});return t.title.icon=r.textEditorIcon,new G({content:t,context:e,commands:this._commands,translator:this.translator})}}var X,Z=n(1258),ee=n(962),te=n(3559),ne=n(4717),se=n(1840),oe=n(1952);class ie{constructor(e){this._contentChanged=new se.Signal(this),this._stateChanged=new se.Signal(this),this._isDisposed=!1,this._problemChanged=new se.Signal(this),this._submissionsChanged=new se.Signal(this),this._submissionStatus={inProgress:!1,runCount:0,totalCount:0},this._submissionStatusChanged=new se.Signal(this),this.modelDB=new ne.ModelDB,this.sharedModel=new ie.YJudge,this.sharedModel.changed.connect((async(e,t)=>{t.problemIdChange&&(this._problem=await this._problemProvider.getProblem(t.problemIdChange),this._problemChanged.emit(this._problem))})),this._codeModel=new oe.CodeCellModel({}),this._codeModel.mimeType="text/x-python",this.sharedModel.ycodeCellChanged.connect(((e,t)=>{this._codeModel.switchSharedModel(t,!0)})),this._problem=null,this._problemProvider=e}get contentChanged(){return this._contentChanged}get stateChanged(){return this._stateChanged}get dirty(){return this.sharedModel.dirty}set dirty(e){e!==this.dirty&&(this.sharedModel.dirty=e)}get readOnly(){return!1}set readOnly(e){}get isDisposed(){return this._isDisposed}dispose(){this.isDisposed||(this._isDisposed=!0,se.Signal.clearData(this))}initialize(){}get defaultKernelName(){return`Judge: Problem ${this.sharedModel.getProblemId()}`}get defaultKernelLanguage(){return"python"}get codeModel(){return this._codeModel}get source(){return this.sharedModel.getSource()}set source(e){this.sharedModel.setSource(e)}get outputAreaModel(){return this._codeModel.outputs}get problem(){return this._problem}get problemChanged(){return this._problemChanged}async submissions(){return await this._problemProvider.getSubmissions(this.sharedModel.getProblemId())}get submissionsChanged(){return this._submissionsChanged}get submissionStatus(){return this._submissionStatus}set submissionStatus(e){this._submissionStatus=e,this._submissionStatusChanged.emit(this._submissionStatus)}get submissionStatusChanged(){return this._submissionStatusChanged}toString(){return JSON.stringify(this.toJSON())}fromString(e){try{this.fromJSON(JSON.parse(e))}catch(e){if(!(e instanceof SyntaxError))throw e;this.fromJSON({problem_id:"",code:"",judge_format:1})}}toJSON(){return{problem_id:this.sharedModel.getProblemId(),code:this.sharedModel.getSource(),judge_format:1}}fromJSON(e){var t,n;this.sharedModel.createCellModelFromSource(null!==(t=e.code)&&void 0!==t?t:"# 파일이 손상되었습니다. 파일을 삭제하고 새로 생성해주세요."),this.sharedModel.setProblemId(null!==(n=e.problem_id)&&void 0!==n?n:"")}async getTestCases(){return await this._problemProvider.getTestCases(this.sharedModel.getProblemId())}async validate(e){return await this._problemProvider.validate(this.sharedModel.getProblemId(),e)}async submit(e){const t=await this._problemProvider.submit(e);return this._submissionsChanged.emit(await this._problemProvider.getSubmissions(this.sharedModel.getProblemId())),t}}async function re(e,t,n){const s=await e.getProblem(n);if(s){const o=s.title,i=`${p}:${b}/${n}/${o}.judge`,r=`${p}:${b}`;await t.services.contents.save(r,{name:r,type:"directory"});const a=`${p}:${b}/${n}`;return await t.services.contents.save(a,{name:a,type:"directory"}),await async function(e,t,n,s){try{await t.services.contents.get(n)}catch(o){throw o instanceof Z.ServerConnection.ResponseError&&404===o.response.status&&await t.services.contents.save(n,{name:n,type:"file",format:"text",content:await ie.newFileContent(e,s)}),o}finally{return t.openOrReveal(n)}}(e,t,i,n)}}!function(e){e.JudgeModelFactory=class{constructor(e){this._disposed=!1,this._problemProviderFactory=e.problemProviderFactory}get name(){return"judge-model"}get contentType(){return"file"}get fileFormat(){return"text"}get isDisposed(){return this._disposed}dispose(){this._disposed=!0}preferredLanguage(e){return"python"}createNew(t,n){return new e(this._problemProviderFactory())}};class t extends ee.F1{constructor(){super(),this.undoManager=new te.UndoManager([this._cell()],{trackedOrigins:new Set([this])}),this._yproblemId=this.ydoc.getText("problemId"),this._ycodeCellChanged=new se.Signal(this),this._yproblemId.observe((e=>{this._changed.emit({problemIdChange:this.getProblemId()})})),this._ycodeCell=null,this._cell().observe(((e,t)=>{e.changes.keys.get("id")&&this._switchCodeCell(this._cell())}))}createCellModelFromSource(e){this.transact((()=>{const t=this._cell();t.set("source",new te.Text(e)),t.set("metadata",{}),t.set("cell_type","code"),t.set("id",""),t.set("execution_count",0),t.set("outputs",new te.Array)})),this._switchCodeCell(this._cell())}_cell(){return this.ydoc.getMap("cell")}_switchCodeCell(e){const t=this._ycodeCell;this._ycodeCell=new n(e,this),this._ycodeCell.undoManager=this.undoManager,this.undoManager.clear(),this._ycodeCellChanged.emit(this._ycodeCell),this._ycodeCell.changed.connect(((e,t)=>{t.sourceChange&&(this.dirty=!0)})),null==t||t.dispose()}get changed(){return this._changed}get ycodeCellChanged(){return this._ycodeCellChanged}dispose(){}get yCodeCell(){return this._ycodeCell}getProblemId(){return this._yproblemId.toString()}setProblemId(e){this.transact((()=>{const t=this._yproblemId;t.delete(0,t.length),t.insert(0,e)}))}getSource(){var e,t;return null!==(t=null===(e=this._ycodeCell)||void 0===e?void 0:e.getSource())&&void 0!==t?t:""}setSource(e){this._ycodeCell&&this._ycodeCell.setSource(e)}}e.YJudge=t;class n extends ee.B5{constructor(e,t){super(e),this._yjudge=t}get awareness(){return this._yjudge.awareness}}e.newFileContent=async function(e,t){var n,s;const o={problem_id:t,code:null!==(s=null===(n=await e.getProblem(t))||void 0===n?void 0:n.skeletonCode)&&void 0!==s?s:"# 여기에 입력하세요",judge_format:1};return JSON.stringify(o)}}(ie||(ie={})),function(e){e.open=`${_}:plugin:open`,e.openOrCreateFromId=`${_}:plugin:open-or-create-from-id`,e.execute=`${_}:plugin:execute`}(X||(X={}));var ae=n(5149),le=n(3535),de=n(5705),ue=n(1598),ce=n(1526);const me=new ce.Token(`${_}:IProblemProviderRegistry`),he=new ce.Token(`${_}:IJudgePanelFactoryRegistry`),ge=new ce.Token(`${_}:IJudgeSignal`),pe=new se.Signal({}),be={id:`${_}:IJudgeSignal`,provides:ge,activate:e=>({get submitted(){return pe}}),autoStart:!0};let _e=new class{constructor(){this.problems={1:{id:"1",title:"덧셈",timeout:1,inputTransferType:"one_line",skeletonCode:null,content:"\n  # 덧셈\n  ## 문제\n  두 정수 A와 B를 입력받은 다음, A+B를 출력하는 프로그램을 작성하시오.\n  ## 입력\n  첫째 줄에 A와 B가 주어진다. (0 < A, B < 10)\n  ## 출력\n  첫째 줄에 A+B를 출력한다.\n          ",userId:null,testCases:["2 4","6 12","10000 21111","-1234 30"],outputs:["6","18","31111","-1204"]},2:{id:"2",title:"작은 별",timeout:1,inputTransferType:"one_line",skeletonCode:null,content:"\n  # 작은 별\n  ## 문제\n  정수 N을 입력받은 다음 다음과 같이 N줄의 별을 출력하는 프로그램을 작성하시오.\n  ## 입력\n  첫째 줄에 N이 주어진다. (0 < N < 10)\n  ## 출력\n  첫째 줄에는 별 1개, 둘째 줄에는 별 2개, ... N번째 줄에는 별 N개를 출력한다.\n          ",userId:null,testCases:["1","2","4","9"],outputs:["*","*\n**","*\n**\n***\n****","*\n**\n***\n****\n*****\n******\n*******\n********\n*********"]}},this._idToSubmissions={}}async getTestCases(e){return this.problems[e].testCases}async validate(e,t){const n=this.problems[e].outputs;if(n.length!==t.length)return{token:null,totalCount:n.length,acceptedCount:0};let s=0;for(let e=0;e<n.length;e++)n[e].trim()===t[e].trim()&&(s+=1);return{token:null,totalCount:n.length,acceptedCount:s}}async getProblem(e){return this.problems[e]}async getSubmissions(e){var t;return null!==(t=this._idToSubmissions[e])&&void 0!==t?t:[]}async submit(e){void 0===this._idToSubmissions[e.problemId]&&(this._idToSubmissions[e.problemId]=[]);const t=Object.assign(Object.assign({},e),{id:this._idToSubmissions[e.problemId].length.toString(),image:"",userId:"",createdAt:(new Date).toISOString()});return this._idToSubmissions[e.problemId].push(t),t}};const Ce={id:`${_}:IProblemProviderRegistry`,provides:me,activate:e=>({register:e=>{_e=e}}),autoStart:!0};let ye=e=>new Y(e);const we={id:`${_}:IJudgePanelFactoryRegistry`,provides:he,activate:e=>({register:e=>{ye=e}}),autoStart:!0},xe={id:`${_}:plugin`,autoStart:!0,requires:[i.ITranslator,a.IEditorServices,d.IRenderMimeRegistry,ae.IDocumentManager,le.IFileBrowserFactory,de.IMainMenu,o.ICommandPalette],optional:[ue.ISettingRegistry,s.ILayoutRestorer],activate:async(e,t,n,s,i,r,a,l,d,u)=>{const c=t.load(g),m=new o.WidgetTracker({namespace:"judge"}),h=c.__("Judge");let b=null;b=d?(await d.load("@jupyterlab/notebook-extension:tracker")).get("codeCellConfig").composite:{};const _=new V({editorServices:n,rendermime:s,commands:e.commands,editorConfig:b,judgePanelFactory:e=>ye(e),submitted:pe,factoryOptions:{name:h,modelName:"judge-model",fileTypes:["judge"],defaultFor:["judge"],preferKernel:!0,canStartKernel:!0,shutdownOnClose:!0,translator:t}});_.widgetCreated.connect(((e,t)=>{t.context.pathChanged.connect((()=>{m.save(t)})),m.add(t)})),e.docRegistry.addWidgetFactory(_),e.docRegistry.addModelFactory(new ie.JudgeModelFactory({problemProviderFactory:()=>_e})),e.docRegistry.addFileType({name:"judge",contentType:"file",fileFormat:"text",displayName:c.__("Judge File"),extensions:[".judge"],mimeTypes:["text/json","application/json"]}),function(e,t,n,s,o){e.addCommand(X.open,{execute:async e=>{n.openOrReveal(e.path)},label:t.__("Open Judge")}),e.addCommand(X.openOrCreateFromId,{execute:async e=>{e.problemId&&await re(o,n,e.problemId)},label:t.__("Open or Create Judge From Id")}),e.addCommand(X.execute,{execute:async e=>{s.currentWidget&&s.currentWidget.content.execute()},label:t.__("Execute")})}(e.commands,c,i,m,_e),function(e,t,n){!function(e,t){const n={tracker:t,undo:e=>{e.content.editor.undo()},redo:e=>{e.content.editor.redo()}};e.editMenu.undoers.add(n)}(e,t),function(e,t,n){const s={tracker:t,runLabel:e=>n.__("Run Code"),run:async e=>{await e.content.execute()},runAllLabel:e=>n.__("Run All Code"),runAll:async e=>{await e.content.execute()}};e.runMenu.codeRunners.add(s)}(e,t,n)}(a,m,c),l.addItem({command:X.openOrCreateFromId,category:"Judge",args:{problemId:"1"}}),u&&u.restore(m,{command:X.open,args:e=>({path:e.context.path}),name:e=>e.context.path}),e.serviceManager.contents.addDrive(new Z.Drive({name:p})),r.createFileBrowser("judgebrowser",{driveName:p})}},fe=[xe,Ce,we,be]}}]);