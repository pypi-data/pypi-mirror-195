"use strict";
(self["webpackChunkinteractivede"] = self["webpackChunkinteractivede"] || []).push([["lib_index_js"],{

/***/ "./lib/cells/TrrackVisComponent.js":
/*!*****************************************!*\
  !*** ./lib/cells/TrrackVisComponent.js ***!
  \*****************************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   "TrrackVisComponent": () => (/* binding */ TrrackVisComponent)
/* harmony export */ });
/* harmony import */ var _trrack_vis_react__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! @trrack/vis-react */ "webpack/sharing/consume/default/@trrack/vis-react/@trrack/vis-react");
/* harmony import */ var _trrack_vis_react__WEBPACK_IMPORTED_MODULE_0___default = /*#__PURE__*/__webpack_require__.n(_trrack_vis_react__WEBPACK_IMPORTED_MODULE_0__);
/* harmony import */ var react__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! react */ "webpack/sharing/consume/default/react");
/* harmony import */ var react__WEBPACK_IMPORTED_MODULE_1___default = /*#__PURE__*/__webpack_require__.n(react__WEBPACK_IMPORTED_MODULE_1__);


function TrrackVisComponent({ manager }) {
    const { trrack } = manager;
    const [current, setCurrent] = (0,react__WEBPACK_IMPORTED_MODULE_1__.useState)(trrack.current.id);
    const { verticalSpace, marginTop, gutter } = {
        verticalSpace: 25,
        marginTop: 25,
        gutter: 25
    };
    (0,react__WEBPACK_IMPORTED_MODULE_1__.useEffect)(() => {
        const fn = (_, { currentNode }) => {
            setCurrent(currentNode);
        };
        manager.currentChange.connect(fn);
        return () => {
            manager.currentChange.disconnect(fn);
        };
    }, [manager]);
    return (react__WEBPACK_IMPORTED_MODULE_1___default().createElement(_trrack_vis_react__WEBPACK_IMPORTED_MODULE_0__.ProvVis, { root: trrack.root.id, config: {
            changeCurrent: (node) => {
                trrack.to(node);
            },
            labelWidth: 100,
            verticalSpace,
            marginTop,
            marginLeft: 15,
            gutter
        }, nodeMap: trrack.graph.backend.nodes, currentNode: current }));
}


/***/ }),

/***/ "./lib/cells/outputHeader/OutputHeader.js":
/*!************************************************!*\
  !*** ./lib/cells/outputHeader/OutputHeader.js ***!
  \************************************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   "OutputHeader": () => (/* binding */ OutputHeader)
/* harmony export */ });
/* harmony import */ var _jupyterlab_ui_components__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! @jupyterlab/ui-components */ "webpack/sharing/consume/default/@jupyterlab/ui-components");
/* harmony import */ var _jupyterlab_ui_components__WEBPACK_IMPORTED_MODULE_0___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_ui_components__WEBPACK_IMPORTED_MODULE_0__);
/* harmony import */ var jsonpath_plus__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! jsonpath-plus */ "webpack/sharing/consume/default/jsonpath-plus/jsonpath-plus");
/* harmony import */ var jsonpath_plus__WEBPACK_IMPORTED_MODULE_1___default = /*#__PURE__*/__webpack_require__.n(jsonpath_plus__WEBPACK_IMPORTED_MODULE_1__);
/* harmony import */ var react__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! react */ "webpack/sharing/consume/default/react");
/* harmony import */ var react__WEBPACK_IMPORTED_MODULE_2___default = /*#__PURE__*/__webpack_require__.n(react__WEBPACK_IMPORTED_MODULE_2__);
/* harmony import */ var _utils__WEBPACK_IMPORTED_MODULE_3__ = __webpack_require__(/*! ../../utils */ "./lib/utils/IDEGlobal.js");
/* eslint-disable @typescript-eslint/no-empty-function */




const OUTPUT_HEADER_BTN_CLASS = 'jp-OutputHeaderWidget-btn';
const dataFrameList = [];
class OutputHeader extends (react__WEBPACK_IMPORTED_MODULE_2___default().Component) {
    constructor(props) {
        super(props);
        const cell = this.props.cell;
        const tManager = _utils__WEBPACK_IMPORTED_MODULE_3__.IDEGlobal.trracks.get(cell.cellId);
        if (!tManager)
            throw new Error("Can't find TrrackManager for cell");
        this.fn = (_, args) => {
            const state = this.state;
            state.reset.disabled = tManager.hasOnlyRoot;
            state.filter.disabled = false;
            this.setState(state);
        };
        tManager.currentChange.connect(this.fn, this);
        this.manager = tManager;
        this.state = {
            reset: {
                disabled: tManager.hasOnlyRoot,
                action: () => tManager.reset()
            },
            filter: {
                disabled: false,
                action: () => filter(this.props.cell)
            },
            dataFrameList
        };
    }
    componentWillUnmount() {
        this.manager.currentChange.disconnect(this.fn, this);
    }
    render() {
        const { reset, filter } = this.state;
        return (react__WEBPACK_IMPORTED_MODULE_2___default().createElement((react__WEBPACK_IMPORTED_MODULE_2___default().Fragment), null,
            react__WEBPACK_IMPORTED_MODULE_2___default().createElement(_jupyterlab_ui_components__WEBPACK_IMPORTED_MODULE_0__.Button, { disabled: reset.disabled, onClick: reset.action, className: OUTPUT_HEADER_BTN_CLASS }, "Reset"),
            react__WEBPACK_IMPORTED_MODULE_2___default().createElement(_jupyterlab_ui_components__WEBPACK_IMPORTED_MODULE_0__.Button, { disabled: filter.disabled, onClick: filter.action, className: OUTPUT_HEADER_BTN_CLASS }, "Filter"),
            react__WEBPACK_IMPORTED_MODULE_2___default().createElement(_jupyterlab_ui_components__WEBPACK_IMPORTED_MODULE_0__.Button, { onClick: () => {
                    var _a, _b, _c, _d;
                    console.clear();
                    const view = _utils__WEBPACK_IMPORTED_MODULE_3__.IDEGlobal.views.get(this.props.cell.cellId);
                    if (!view)
                        return;
                    const dataPaths = (0,jsonpath_plus__WEBPACK_IMPORTED_MODULE_1__.JSONPath)({
                        path: '$..data..name',
                        json: ((_a = view.vega) === null || _a === void 0 ? void 0 : _a.vgSpec) || {},
                        resultType: 'all'
                    });
                    const dataSource = dataPaths.find(d => d.value.includes('source'));
                    const data = (_b = view.vega) === null || _b === void 0 ? void 0 : _b.view.data(dataSource.value);
                    const dataString = JSON.stringify(data);
                    const dfName = `data_${this.manager.current}`;
                    (_d = (_c = _utils__WEBPACK_IMPORTED_MODULE_3__.IDEGlobal.executor) === null || _c === void 0 ? void 0 : _c.execute(`ext_df = pd.read_json('${dataString}')`, {
                        withPandas: true
                    })) === null || _d === void 0 ? void 0 : _d.done.then(() => {
                        if (!this.state.dataFrameList.includes(dfName)) {
                            this.setState(s => ({
                                dataFrameList: [...s.dataFrameList, dfName]
                            }));
                            dataFrameList.push(dfName);
                        }
                    });
                }, className: OUTPUT_HEADER_BTN_CLASS }, "Extract dataframe")));
    }
}
function getAll(cell) {
    const cellId = cell.cellId;
    const vega = _utils__WEBPACK_IMPORTED_MODULE_3__.IDEGlobal.views.get(cellId);
    if (!vega)
        return;
    const trrack = _utils__WEBPACK_IMPORTED_MODULE_3__.IDEGlobal.trracks.get(cellId);
    if (!trrack)
        return;
    return {
        vega,
        trrack
    };
}
async function filter(cell) {
    const managers = getAll(cell);
    if (!managers)
        return;
    const { vega, trrack } = managers;
    if (!vega && !trrack)
        return;
    vega.filter();
}


/***/ }),

/***/ "./lib/cells/outputHeader/OutputHeaderWidget.js":
/*!******************************************************!*\
  !*** ./lib/cells/outputHeader/OutputHeaderWidget.js ***!
  \******************************************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   "OutputHeaderWidget": () => (/* binding */ OutputHeaderWidget)
/* harmony export */ });
/* harmony import */ var _jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! @jupyterlab/apputils */ "webpack/sharing/consume/default/@jupyterlab/apputils");
/* harmony import */ var _jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_0___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_0__);
/* harmony import */ var react__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! react */ "webpack/sharing/consume/default/react");
/* harmony import */ var react__WEBPACK_IMPORTED_MODULE_1___default = /*#__PURE__*/__webpack_require__.n(react__WEBPACK_IMPORTED_MODULE_1__);
/* harmony import */ var _utils__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! ../../utils */ "./lib/utils/IDEGlobal.js");
/* harmony import */ var _OutputHeader__WEBPACK_IMPORTED_MODULE_3__ = __webpack_require__(/*! ./OutputHeader */ "./lib/cells/outputHeader/OutputHeader.js");




const OUTPUT_HEADER_CLASS = 'jp-OutputHeaderWidget';
const OUTPUT_HEADER_HIDE_CLASS = 'jp-OutputHeaderWidget-hide';
class OutputHeaderWidget extends _jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_0__.ReactWidget {
    constructor(_cell) {
        super();
        this._cell = _cell;
        this.addClass(OUTPUT_HEADER_CLASS);
        this._hasVegaPlot = Boolean(_utils__WEBPACK_IMPORTED_MODULE_2__.IDEGlobal.views.get(_cell.cellId));
        this.toggle(this._hasVegaPlot);
    }
    toggle(to) {
        this.toggleClass(OUTPUT_HEADER_HIDE_CLASS, !to);
    }
    render() {
        return this._hasVegaPlot ? react__WEBPACK_IMPORTED_MODULE_1___default().createElement(_OutputHeader__WEBPACK_IMPORTED_MODULE_3__.OutputHeader, { cell: this._cell }) : null;
    }
}
// console.log(window.views.get(id)?.view.getState());
// console.log(window.views.get(id)?.vega.vgSpec);
// const vega: any = window.views.get(id)?.vega;
// // can remove here
// const data_ = vega?.vgSpec.data[1];
// const data = data_.values;
// const params = vega.view.getState().signals['brush'];
// const fields = Object.keys(params);
// const a = params[fields[0]];
// const b = params[fields[1]];
// const filteredData = data.filter((d: any) => {
//   const x = d[fields[0]];
//   const y = d[fields[1]];
//   return x >= a[0] && x <= a[1] && y >= b[0] && y <= b[1];
// });
// window.views.get(id)?.vega.view.remove(data_.name, filteredData);
// window.views.get(id)?.vega.view.runAsync();


/***/ }),

/***/ "./lib/cells/trrack/init.js":
/*!**********************************!*\
  !*** ./lib/cells/trrack/init.js ***!
  \**********************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   "TrrackOps": () => (/* binding */ TrrackOps),
/* harmony export */   "defaultActions": () => (/* binding */ defaultActions)
/* harmony export */ });
/* harmony import */ var _trrack_core__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! @trrack/core */ "webpack/sharing/consume/default/@trrack/core/@trrack/core?4e06");
/* harmony import */ var _trrack_core__WEBPACK_IMPORTED_MODULE_0___default = /*#__PURE__*/__webpack_require__.n(_trrack_core__WEBPACK_IMPORTED_MODULE_0__);

const initialState = {
    msg: 'Hello, World!',
    interactions: []
};
function setupTrrack(loadFrom) {
    const registry = _trrack_core__WEBPACK_IMPORTED_MODULE_0__.Registry.create();
    const testAction = registry.register('test', (state, msg) => {
        state.msg = msg;
    });
    const addInteractionAction = registry.register('interaction', (state, sel) => {
        state.interactions.push(sel);
    });
    let trrack = (0,_trrack_core__WEBPACK_IMPORTED_MODULE_0__.initializeTrrack)({
        registry,
        initialState
    });
    if (loadFrom && typeof loadFrom === 'string') {
        trrack.import(loadFrom);
    }
    else if (loadFrom && typeof loadFrom !== 'string') {
        trrack = (0,_trrack_core__WEBPACK_IMPORTED_MODULE_0__.initializeTrrack)({
            registry,
            initialState: loadFrom
        });
    }
    return {
        trrack,
        actions: {
            testAction,
            addInteractionAction
        }
    };
}
const defaultActions = {
    testAction: (0,_trrack_core__WEBPACK_IMPORTED_MODULE_0__.createAction)('test'),
    addInteractionAction: (0,_trrack_core__WEBPACK_IMPORTED_MODULE_0__.createAction)('select')
};
/**
 * A namespace for Trrack statics.
 */
class TrrackOps {
    /**
     * Create a Trrack and TrrackActions for a cell
     * @returns Trrack instance and actions
     */
    static create(savedGraph) {
        return setupTrrack(savedGraph);
    }
}


/***/ }),

/***/ "./lib/cells/trrack/trrackManager.js":
/*!*******************************************!*\
  !*** ./lib/cells/trrack/trrackManager.js ***!
  \*******************************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   "TrrackManager": () => (/* binding */ TrrackManager)
/* harmony export */ });
/* harmony import */ var _lumino_signaling__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! @lumino/signaling */ "webpack/sharing/consume/default/@lumino/signaling");
/* harmony import */ var _lumino_signaling__WEBPACK_IMPORTED_MODULE_0___default = /*#__PURE__*/__webpack_require__.n(_lumino_signaling__WEBPACK_IMPORTED_MODULE_0__);
/* harmony import */ var _utils__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! ../../utils */ "./lib/utils/disposable.js");
/* harmony import */ var _utils__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! ../../utils */ "./lib/utils/IDEGlobal.js");
/* harmony import */ var _init__WEBPACK_IMPORTED_MODULE_3__ = __webpack_require__(/*! ./init */ "./lib/cells/trrack/init.js");



const TRRACK_GRAPH_KEY = 'trrack_graph';
class TrrackManager extends _utils__WEBPACK_IMPORTED_MODULE_1__.Disposable {
    constructor(_cell) {
        super();
        this._cell = _cell;
        this._trrackInstanceChange = new _lumino_signaling__WEBPACK_IMPORTED_MODULE_0__.Signal(this);
        this._trrackCurrentChange = new _lumino_signaling__WEBPACK_IMPORTED_MODULE_0__.Signal(this);
        const { trrack, actions } = this._reset(true);
        this._trrack = trrack;
        this._actions = actions;
    }
    get savedGraph() {
        var _a;
        return (_a = this._cell.model.metadata) === null || _a === void 0 ? void 0 : _a.get(TRRACK_GRAPH_KEY);
    }
    get trrack() {
        return this._trrack;
    }
    get actions() {
        return this._actions;
    }
    get isAtRoot() {
        return this.current === this.root;
    }
    get isAtLatest() {
        return this._trrack.current.children.length === 0;
    }
    get hasOnlyRoot() {
        return this._trrack.root.children.length === 0;
    }
    get changed() {
        return this._trrackInstanceChange;
    }
    get currentChange() {
        return this._trrackCurrentChange;
    }
    get root() {
        return this._trrack.root.id;
    }
    get current() {
        return this._trrack.current.id;
    }
    async addInteraction(interaction, label) {
        await this.trrack.apply(label ? label : interaction.type, this.actions.addInteractionAction(interaction));
    }
    _reset(loadGraph) {
        if (this._trrack) {
            _utils__WEBPACK_IMPORTED_MODULE_2__.IDEGlobal.trracks["delete"](this._cell.cellId);
        }
        console.log('reset');
        this.currentChange.disconnect(this._saveTrrackGraphToModel, this);
        const { trrack, actions } = _init__WEBPACK_IMPORTED_MODULE_3__.TrrackOps.create(loadGraph ? this.savedGraph : undefined);
        this._trrack = trrack;
        this._actions = actions;
        this._saveTrrackGraphToModel();
        this._trrack.currentChange(() => {
            this._trrackCurrentChange.emit({
                currentNode: this._trrack.current.id,
                state: this._trrack.getState()
            });
        });
        this.currentChange.connect(this._saveTrrackGraphToModel, this);
        this._trrackInstanceChange.emit(this._trrack.root.id);
        this._trrackCurrentChange.emit({
            currentNode: this._trrack.current.id,
            state: this._trrack.getState()
        });
        return { trrack, actions };
    }
    _saveTrrackGraphToModel() {
        this._cell.model.metadata.set(TRRACK_GRAPH_KEY, this._trrack.export());
        _utils__WEBPACK_IMPORTED_MODULE_2__.IDEGlobal.trracks.set(this._cell.cellId, this);
    }
    reset() {
        this._reset(false);
    }
    dispose() {
        if (this.isDisposed) {
            return;
        }
        this.isDisposed = true;
        _utils__WEBPACK_IMPORTED_MODULE_2__.IDEGlobal.trracks["delete"](this._cell.cellId);
        _lumino_signaling__WEBPACK_IMPORTED_MODULE_0__.Signal.clearData(this);
    }
}


/***/ }),

/***/ "./lib/cells/trrack/vega/helpers.js":
/*!******************************************!*\
  !*** ./lib/cells/trrack/vega/helpers.js ***!
  \******************************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   "getQueryStringFromSelectionInterval": () => (/* binding */ getQueryStringFromSelectionInterval),
/* harmony export */   "getRangeFromSelectionInterval": () => (/* binding */ getRangeFromSelectionInterval)
/* harmony export */ });
function getQueryStringFromSelectionInterval({ params: { selection } }) {
    const subQueries = [];
    Object.entries(selection).forEach(([dimension, range]) => {
        subQueries.push(`${Math.round(range[0] * 1000) / 1000} <= ${dimension} <= ${Math.round(range[1] * 1000) / 1000}`);
    });
    return subQueries.filter(q => q.length > 0).length > 0
        ? subQueries.join(' & ')
        : '';
}
function getRangeFromSelectionInterval(init) {
    const ranges = [];
    Object.entries(init).forEach(([dimension, range]) => {
        ranges.push({
            field: dimension,
            range
        });
    });
    return ranges;
}


/***/ }),

/***/ "./lib/cells/trrack/vega/listeners.js":
/*!********************************************!*\
  !*** ./lib/cells/trrack/vega/listeners.js ***!
  \********************************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   "getSelectionIntervalListener": () => (/* binding */ getSelectionIntervalListener)
/* harmony export */ });
/* harmony import */ var _lumino_coreutils__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! @lumino/coreutils */ "webpack/sharing/consume/default/@lumino/coreutils");
/* harmony import */ var _lumino_coreutils__WEBPACK_IMPORTED_MODULE_0___default = /*#__PURE__*/__webpack_require__.n(_lumino_coreutils__WEBPACK_IMPORTED_MODULE_0__);
/* harmony import */ var fast_json_patch__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! fast-json-patch */ "webpack/sharing/consume/default/fast-json-patch/fast-json-patch");
/* harmony import */ var fast_json_patch__WEBPACK_IMPORTED_MODULE_1___default = /*#__PURE__*/__webpack_require__.n(fast_json_patch__WEBPACK_IMPORTED_MODULE_1__);
/* harmony import */ var _utils__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! ../../../utils */ "./lib/utils/IDEGlobal.js");
/* harmony import */ var _utils__WEBPACK_IMPORTED_MODULE_3__ = __webpack_require__(/*! ../../../utils */ "./lib/utils/debounce.js");



function getSelectionIntervalListener({ manager, spec, selectionPath, trrackManager, cellId }) {
    const selector = selectionPath.parentProperty;
    const path = selectionPath.pointer;
    const { view, vegaRenderer } = manager;
    if (!vegaRenderer || !view)
        throw new Error('Vega or view not found');
    const cell = _utils__WEBPACK_IMPORTED_MODULE_2__.IDEGlobal.cells.get(cellId);
    if (!cell)
        throw new Error("Cell doesn't exist");
    return (0,_utils__WEBPACK_IMPORTED_MODULE_3__.debounce)(async () => {
        const state = view.getState();
        const signals = state.signals;
        const params = {
            selection: signals[selector],
            x: signals[`${selector}_x`],
            y: signals[`${selector}_y`]
        };
        const selectionInit = {};
        Object.entries(params.selection).forEach(([dim, range]) => {
            selectionInit[dim] = range;
        });
        const newSpec = applyInitToSelection(selectionInit, spec, path);
        const selection = {
            id: _lumino_coreutils__WEBPACK_IMPORTED_MODULE_0__.UUID.uuid4(),
            type: 'selection_interval',
            name: selector,
            path,
            params,
            spec: newSpec
        };
        await trrackManager.addInteraction(selection, 'Brush selection');
        cell.updateVegaSpec(newSpec);
    });
}
function applyInitToSelection(init, spec, path) {
    const newSpec = (0,fast_json_patch__WEBPACK_IMPORTED_MODULE_1__.applyPatch)(JSON.parse(JSON.stringify(spec)), [
        {
            op: 'replace',
            path: `${path}/init`,
            value: (0,fast_json_patch__WEBPACK_IMPORTED_MODULE_1__.deepClone)(init)
        }
    ]);
    return newSpec.newDocument;
}


/***/ }),

/***/ "./lib/cells/trrack/vega/vegaManager.js":
/*!**********************************************!*\
  !*** ./lib/cells/trrack/vega/vegaManager.js ***!
  \**********************************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   "VegaManager": () => (/* binding */ VegaManager)
/* harmony export */ });
/* harmony import */ var _lumino_coreutils__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! @lumino/coreutils */ "webpack/sharing/consume/default/@lumino/coreutils");
/* harmony import */ var _lumino_coreutils__WEBPACK_IMPORTED_MODULE_0___default = /*#__PURE__*/__webpack_require__.n(_lumino_coreutils__WEBPACK_IMPORTED_MODULE_0__);
/* harmony import */ var _lumino_signaling__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! @lumino/signaling */ "webpack/sharing/consume/default/@lumino/signaling");
/* harmony import */ var _lumino_signaling__WEBPACK_IMPORTED_MODULE_1___default = /*#__PURE__*/__webpack_require__.n(_lumino_signaling__WEBPACK_IMPORTED_MODULE_1__);
/* harmony import */ var fast_json_patch__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! fast-json-patch */ "webpack/sharing/consume/default/fast-json-patch/fast-json-patch");
/* harmony import */ var fast_json_patch__WEBPACK_IMPORTED_MODULE_2___default = /*#__PURE__*/__webpack_require__.n(fast_json_patch__WEBPACK_IMPORTED_MODULE_2__);
/* harmony import */ var jsonpath_plus__WEBPACK_IMPORTED_MODULE_3__ = __webpack_require__(/*! jsonpath-plus */ "webpack/sharing/consume/default/jsonpath-plus/jsonpath-plus");
/* harmony import */ var jsonpath_plus__WEBPACK_IMPORTED_MODULE_3___default = /*#__PURE__*/__webpack_require__.n(jsonpath_plus__WEBPACK_IMPORTED_MODULE_3__);
/* harmony import */ var _utils__WEBPACK_IMPORTED_MODULE_4__ = __webpack_require__(/*! ../../../utils */ "./lib/utils/disposable.js");
/* harmony import */ var _utils__WEBPACK_IMPORTED_MODULE_5__ = __webpack_require__(/*! ../../../utils */ "./lib/utils/IDEGlobal.js");
/* harmony import */ var _helpers__WEBPACK_IMPORTED_MODULE_7__ = __webpack_require__(/*! ./helpers */ "./lib/cells/trrack/vega/helpers.js");
/* harmony import */ var _listeners__WEBPACK_IMPORTED_MODULE_6__ = __webpack_require__(/*! ./listeners */ "./lib/cells/trrack/vega/listeners.js");







class VegaManager extends _utils__WEBPACK_IMPORTED_MODULE_4__.Disposable {
    constructor(cellId, vegaRenderer, initVegaSpec) {
        super();
        this.vegaRenderer = vegaRenderer;
        this._listeners = {};
        VegaManager.disposePrevious();
        VegaManager.previous.push(this);
        this._cellId = cellId;
        const _tManager = _utils__WEBPACK_IMPORTED_MODULE_5__.IDEGlobal.trracks.get(cellId);
        if (!_tManager) {
            throw new Error('No trrack manager found');
        }
        this._tManager = _tManager;
        _utils__WEBPACK_IMPORTED_MODULE_5__.IDEGlobal.views.set(cellId, this);
        const cell = _utils__WEBPACK_IMPORTED_MODULE_5__.IDEGlobal.cells.get(cellId);
        if (!cell)
            throw new Error("Cell doesn't exist");
        this._cell = cell;
        this._originalVegaSpec = cell.getoriginalSpec() || initVegaSpec;
        cell.saveOriginalSpec(this._originalVegaSpec);
        this._tManager.currentChange.connect(() => {
            const interactions = (0,fast_json_patch__WEBPACK_IMPORTED_MODULE_2__.deepClone)(this._tManager.trrack.getState().interactions);
            const interaction = interactions.pop();
            cell.updateVegaSpec(interaction ? interaction.spec : this._originalVegaSpec);
        }, this);
    }
    static init(cellId, renderedVega, spec) {
        return new VegaManager(cellId, renderedVega, spec);
    }
    static disposePrevious() {
        this.previous.forEach(v => v.dispose());
        this.previous = [];
    }
    dispose() {
        var _a;
        if (this.isDisposed)
            return;
        _lumino_signaling__WEBPACK_IMPORTED_MODULE_1__.Signal.disconnectReceiver(this);
        this.isDisposed = true;
        (_a = this.view) === null || _a === void 0 ? void 0 : _a.finalize();
        _utils__WEBPACK_IMPORTED_MODULE_5__.IDEGlobal.views["delete"](this._cellId);
    }
    get vega() {
        var _a;
        return (_a = this.vegaRenderer) === null || _a === void 0 ? void 0 : _a.vega;
    }
    get view() {
        var _a;
        return (_a = this.vega) === null || _a === void 0 ? void 0 : _a.view;
    }
    get spec() {
        return (this.vega ? this.vega.spec : this._originalVegaSpec);
    }
    async removeBrushes() {
        // for (const selector in (this.spec as any).selection) {
        //   await this.applySelectionInterval(selector, {
        //     x: [],
        //     y: [],
        //     selection: {}
        //   });
        // }
    }
    addListeners() {
        this.addSelectionListeners();
    }
    addSelectionListeners() {
        if (!this.view)
            return;
        this.removeSelectionListeners();
        const selectionPaths = (0,jsonpath_plus__WEBPACK_IMPORTED_MODULE_3__.JSONPath)({
            path: '$..selection[?(@parentProperty !== "encoding")]',
            json: this.spec,
            resultType: 'all'
        });
        for (let i = 0; i < selectionPaths.length; ++i) {
            const selectionPath = selectionPaths[i];
            const type = selectionPath.value.type;
            const selector = selectionPath.parentProperty;
            if (type === 'interval') {
                const listener = (0,_listeners__WEBPACK_IMPORTED_MODULE_6__.getSelectionIntervalListener)({
                    manager: this,
                    spec: this.spec,
                    selectionPath,
                    trrackManager: this._tManager,
                    cellId: this._cellId
                });
                this._listeners[selector] = listener;
                this.view.addSignalListener(selector, listener);
            }
        }
    }
    removeListeners() {
        this.removeSelectionListeners();
    }
    removeSelectionListeners() {
        var _a;
        // Wrong
        for (const selector in this._listeners) {
            (_a = this.view) === null || _a === void 0 ? void 0 : _a.removeSignalListener(selector, this._listeners[selector]);
        }
    }
    filter() {
        const spec = this.spec;
        const interactions = this._tManager.trrack
            .getState()
            .interactions.filter(i => i.type === 'selection_interval');
        if (interactions.length === 0)
            return;
        spec.transform = spec.transform || [];
        const filters = [];
        const selectionPaths = (0,jsonpath_plus__WEBPACK_IMPORTED_MODULE_3__.JSONPath)({
            path: '$..selection[?(@parentProperty !== "encoding")]',
            json: this.spec,
            resultType: 'all'
        });
        const removeOps = [];
        for (let i = 0; i < selectionPaths.length; ++i) {
            const selectionPath = selectionPaths[i];
            const value = selectionPath.value;
            const init = value === null || value === void 0 ? void 0 : value.init;
            const type = selectionPath.value.type;
            if (init) {
                if (type === 'interval') {
                    filters.push({
                        not: {
                            and: (0,_helpers__WEBPACK_IMPORTED_MODULE_7__.getRangeFromSelectionInterval)(init)
                        }
                    });
                }
                removeOps.push({
                    op: 'remove',
                    path: `${selectionPath.pointer}/init`
                });
            }
        }
        const filterPaths = (0,jsonpath_plus__WEBPACK_IMPORTED_MODULE_3__.JSONPath)({
            path: '$..transform[?(@.filter)]',
            json: this.spec,
            resultType: 'all'
        });
        const previousFilters = [].concat(...filterPaths.map(p => p.value.filter.and));
        console.log(filters);
        console.log(previousFilters);
        console.log([...filters, ...previousFilters]);
        const newSpec = (0,fast_json_patch__WEBPACK_IMPORTED_MODULE_2__.applyPatch)((0,fast_json_patch__WEBPACK_IMPORTED_MODULE_2__.deepClone)(spec), (0,fast_json_patch__WEBPACK_IMPORTED_MODULE_2__.deepClone)([
            ...removeOps,
            {
                op: 'add',
                path: '/transform',
                value: []
            },
            {
                op: 'add',
                path: '/transform/0',
                value: {
                    filter: {}
                }
            },
            {
                op: 'add',
                path: '/transform/0/filter',
                value: {
                    and: [...filters, ...previousFilters]
                }
            }
        ])).newDocument;
        this._tManager.addInteraction({
            id: _lumino_coreutils__WEBPACK_IMPORTED_MODULE_0__.UUID.uuid4(),
            type: 'filter',
            path: '',
            spec: newSpec
        });
        this._cell.updateVegaSpec(newSpec);
    }
}
VegaManager.previous = [];


/***/ }),

/***/ "./lib/cells/trrackableCell.js":
/*!*************************************!*\
  !*** ./lib/cells/trrackableCell.js ***!
  \*************************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   "TrrackableCell": () => (/* binding */ TrrackableCell)
/* harmony export */ });
/* harmony import */ var _jupyterlab_cells__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! @jupyterlab/cells */ "webpack/sharing/consume/default/@jupyterlab/cells");
/* harmony import */ var _jupyterlab_cells__WEBPACK_IMPORTED_MODULE_0___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_cells__WEBPACK_IMPORTED_MODULE_0__);
/* harmony import */ var _jupyterlab_vega5_extension__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! @jupyterlab/vega5-extension */ "webpack/sharing/consume/default/@jupyterlab/vega5-extension");
/* harmony import */ var _jupyterlab_vega5_extension__WEBPACK_IMPORTED_MODULE_1___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_vega5_extension__WEBPACK_IMPORTED_MODULE_1__);
/* harmony import */ var _lumino_signaling__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! @lumino/signaling */ "webpack/sharing/consume/default/@lumino/signaling");
/* harmony import */ var _lumino_signaling__WEBPACK_IMPORTED_MODULE_2___default = /*#__PURE__*/__webpack_require__.n(_lumino_signaling__WEBPACK_IMPORTED_MODULE_2__);
/* harmony import */ var _constants__WEBPACK_IMPORTED_MODULE_6__ = __webpack_require__(/*! ../constants */ "./lib/constants.js");
/* harmony import */ var _utils__WEBPACK_IMPORTED_MODULE_4__ = __webpack_require__(/*! ../utils */ "./lib/utils/IDEGlobal.js");
/* harmony import */ var _outputHeader_OutputHeaderWidget__WEBPACK_IMPORTED_MODULE_5__ = __webpack_require__(/*! ./outputHeader/OutputHeaderWidget */ "./lib/cells/outputHeader/OutputHeaderWidget.js");
/* harmony import */ var _trrack_trrackManager__WEBPACK_IMPORTED_MODULE_3__ = __webpack_require__(/*! ./trrack/trrackManager */ "./lib/cells/trrack/trrackManager.js");







class TrrackableCell extends _jupyterlab_cells__WEBPACK_IMPORTED_MODULE_0__.CodeCell {
    constructor(options) {
        super(options);
        this._trrackManager = new _trrack_trrackManager__WEBPACK_IMPORTED_MODULE_3__.TrrackManager(this); // Setup trrack manager
        _utils__WEBPACK_IMPORTED_MODULE_4__.IDEGlobal.cells.set(this.cellId, this);
        this.model.outputs.fromJSON(this.model.outputs.toJSON()); // Update outputs to trigger rerender
        this.model.outputs.changed.connect(this._outputChangeListener, this); // Add listener for when output changes
        if (!this._trrackChangeHandler)
            this._trrackManager.changed.connect(
            // Add a listener for when trrack instance changes
            this._trrackChangeHandler, this);
    }
    dispose() {
        if (this.isDisposed) {
            return;
        }
        _lumino_signaling__WEBPACK_IMPORTED_MODULE_2__.Signal.clearData(this);
        _utils__WEBPACK_IMPORTED_MODULE_4__.IDEGlobal.cells["delete"](this.cellId);
        this._trrackManager.dispose();
        super.dispose();
    }
    get cellId() {
        return this.model.id;
    }
    get trrackId() {
        return this._trrackManager.root;
    }
    get trrackManager() {
        return this._trrackManager;
    }
    /**
     * Get the output area widget to setup
     */
    addOutputWidget(layout) {
        const nWidgets = layout.widgets.length;
        if (nWidgets < 2 || nWidgets > 3)
            throw new Error('Unexpected number of widgets in output area');
        if (nWidgets === 3)
            layout.removeWidgetAt(0);
        const widget = new _outputHeader_OutputHeaderWidget__WEBPACK_IMPORTED_MODULE_5__.OutputHeaderWidget(this);
        layout.insertWidget(0, widget);
    }
    // Trrack
    _trrackChangeHandler() {
        const outputs = this.model.outputs.toJSON();
        const executeResultOutputIdx = outputs.findIndex(o => o.output_type === 'execute_result');
        if (executeResultOutputIdx === -1)
            return;
        const output = this.model.outputs.get(executeResultOutputIdx);
        if (output.type !== 'execute_result')
            return;
        output.setData({
            // Wrong
            data: output.data,
            metadata: output.metadata || {}
        });
    }
    saveOriginalSpec(spec) {
        this.model.metadata.set('original_spec', spec);
    }
    getoriginalSpec() {
        return this.model.metadata.get('original_spec');
    }
    updateVegaSpec(spec) {
        const outputs = this.model.outputs.toJSON();
        const executeResultOutputIdx = outputs.findIndex(o => o.output_type === 'execute_result');
        if (executeResultOutputIdx === -1)
            return;
        const output = this.model.outputs.get(executeResultOutputIdx);
        if (output.type !== 'execute_result')
            return;
        output.setData({
            data: {
                [_constants__WEBPACK_IMPORTED_MODULE_6__.TRRACK_MIME_TYPE]: {
                    [_jupyterlab_vega5_extension__WEBPACK_IMPORTED_MODULE_1__.VEGALITE4_MIME_TYPE]: spec,
                    [_constants__WEBPACK_IMPORTED_MODULE_6__.TRRACK_GRAPH_MIME_TYPE]: this.cellId
                }
            },
            metadata: output.metadata || {}
        });
    }
    _outputChangeListener(model, { type, newIndex }) {
        if (type !== 'add')
            return;
        const output = model.get(newIndex);
        if (output.type === 'execute_result') {
            if (output.data[_constants__WEBPACK_IMPORTED_MODULE_6__.TRRACK_MIME_TYPE])
                return;
            output.setData({
                data: {
                    [_constants__WEBPACK_IMPORTED_MODULE_6__.TRRACK_MIME_TYPE]: {
                        ...output.data,
                        [_constants__WEBPACK_IMPORTED_MODULE_6__.TRRACK_GRAPH_MIME_TYPE]: this.cellId
                    }
                },
                metadata: output.metadata || {}
            });
        }
    }
}


/***/ }),

/***/ "./lib/cells/trrackableCellFactory.js":
/*!********************************************!*\
  !*** ./lib/cells/trrackableCellFactory.js ***!
  \********************************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   "TrrackableCellFactory": () => (/* binding */ TrrackableCellFactory)
/* harmony export */ });
/* harmony import */ var _jupyterlab_notebook__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! @jupyterlab/notebook */ "webpack/sharing/consume/default/@jupyterlab/notebook");
/* harmony import */ var _jupyterlab_notebook__WEBPACK_IMPORTED_MODULE_0___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_notebook__WEBPACK_IMPORTED_MODULE_0__);
/* harmony import */ var _trrackableCell__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! ./trrackableCell */ "./lib/cells/trrackableCell.js");


class TrrackableCellFactory extends _jupyterlab_notebook__WEBPACK_IMPORTED_MODULE_0__.NotebookPanel.ContentFactory {
    createCodeCell(options, _parent) {
        return new _trrackableCell__WEBPACK_IMPORTED_MODULE_1__.TrrackableCell(options).initializeState();
    }
}


/***/ }),

/***/ "./lib/constants.js":
/*!**************************!*\
  !*** ./lib/constants.js ***!
  \**************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   "EXT_ID": () => (/* binding */ EXT_ID),
/* harmony export */   "TRRACK_GRAPH_MIME_TYPE": () => (/* binding */ TRRACK_GRAPH_MIME_TYPE),
/* harmony export */   "TRRACK_MIME_TYPE": () => (/* binding */ TRRACK_MIME_TYPE)
/* harmony export */ });
const EXT_ID = 'interactivede:uuid';
const TRRACK_GRAPH_MIME_TYPE = 'application/vnd.trrack.graph+json';
const TRRACK_MIME_TYPE = 'application/vnd.trrack+json';


/***/ }),

/***/ "./lib/extension/cellFactoryPlugin.js":
/*!********************************************!*\
  !*** ./lib/extension/cellFactoryPlugin.js ***!
  \********************************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   "cellFactoryPlugin": () => (/* binding */ cellFactoryPlugin)
/* harmony export */ });
/* harmony import */ var _jupyterlab_notebook__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! @jupyterlab/notebook */ "webpack/sharing/consume/default/@jupyterlab/notebook");
/* harmony import */ var _jupyterlab_notebook__WEBPACK_IMPORTED_MODULE_0___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_notebook__WEBPACK_IMPORTED_MODULE_0__);
/* harmony import */ var _cells__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! ../cells */ "./lib/cells/trrackableCellFactory.js");
/* harmony import */ var _utils__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! ../utils */ "./lib/utils/logging.js");



const cellFactoryPlugin = {
    id: 'interactivede:cell-factory',
    provides: _jupyterlab_notebook__WEBPACK_IMPORTED_MODULE_0__.NotebookPanel.IContentFactory,
    autoStart: true,
    activate: () => {
        console.log('Jupyterlab extension interactivede is activated! - cell-factory');
        _utils__WEBPACK_IMPORTED_MODULE_1__.LOG.log('Jupyterlab extension interactivede is activated! - cell-factory');
        return new _cells__WEBPACK_IMPORTED_MODULE_2__.TrrackableCellFactory();
    }
};


/***/ }),

/***/ "./lib/extension/nbExtension.js":
/*!**************************************!*\
  !*** ./lib/extension/nbExtension.js ***!
  \**************************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   "NBWidgetExtension": () => (/* binding */ NBWidgetExtension)
/* harmony export */ });
/* harmony import */ var _jupyterlab_vega5_extension__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! @jupyterlab/vega5-extension */ "webpack/sharing/consume/default/@jupyterlab/vega5-extension");
/* harmony import */ var _jupyterlab_vega5_extension__WEBPACK_IMPORTED_MODULE_0___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_vega5_extension__WEBPACK_IMPORTED_MODULE_0__);
/* harmony import */ var _constants__WEBPACK_IMPORTED_MODULE_3__ = __webpack_require__(/*! ../constants */ "./lib/constants.js");
/* harmony import */ var _notebook_kernel__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! ../notebook/kernel */ "./lib/notebook/kernel/exec.js");
/* harmony import */ var _renderers__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! ../renderers */ "./lib/renderers/vegaRenderer.js");
/* harmony import */ var _renderers__WEBPACK_IMPORTED_MODULE_4__ = __webpack_require__(/*! ../renderers */ "./lib/renderers/trrackOutputRenderer.js");
/* harmony import */ var _renderers__WEBPACK_IMPORTED_MODULE_5__ = __webpack_require__(/*! ../renderers */ "./lib/renderers/trrackGraphRenderer.js");
/* harmony import */ var _utils__WEBPACK_IMPORTED_MODULE_6__ = __webpack_require__(/*! ../utils */ "./lib/utils/IDEGlobal.js");





class NBWidgetExtension {
    constructor(nbTracker) {
        _notebook_kernel__WEBPACK_IMPORTED_MODULE_1__.Executor.init(nbTracker);
    }
    // Called automatically. Do setup here
    createNew(nb, _ctx) {
        // Add a new renderer for vega. Which wraps the original renderer
        nb.content.rendermime.addFactory({
            ..._jupyterlab_vega5_extension__WEBPACK_IMPORTED_MODULE_0__.rendererFactory,
            defaultRank: (_jupyterlab_vega5_extension__WEBPACK_IMPORTED_MODULE_0__.rendererFactory.defaultRank || 10) - 1,
            createRenderer: options => new _renderers__WEBPACK_IMPORTED_MODULE_2__.RenderedVega2(options)
        });
        // Add a renderer for a new mime type called trrack which just wraps cell execution result with trrackId
        nb.content.rendermime.addFactory({
            safe: true,
            mimeTypes: [_constants__WEBPACK_IMPORTED_MODULE_3__.TRRACK_MIME_TYPE],
            defaultRank: 10,
            createRenderer: options => new _renderers__WEBPACK_IMPORTED_MODULE_4__.RenderedTrrackOutput(options)
        });
        // Add a renderer for a new mime type called trrack-graph which which renders a trrack graph from trrackId
        nb.content.rendermime.addFactory({
            safe: true,
            mimeTypes: [_constants__WEBPACK_IMPORTED_MODULE_3__.TRRACK_GRAPH_MIME_TYPE],
            defaultRank: 10,
            createRenderer: options => new _renderers__WEBPACK_IMPORTED_MODULE_5__.RenderedTrrackGraph(options)
        });
        // Init global variables
        _utils__WEBPACK_IMPORTED_MODULE_6__.IDEGlobal.trracks = new Map();
        _utils__WEBPACK_IMPORTED_MODULE_6__.IDEGlobal.views = new Map();
        _utils__WEBPACK_IMPORTED_MODULE_6__.IDEGlobal.cells = new Map();
        _utils__WEBPACK_IMPORTED_MODULE_6__.IDEGlobal.renderMimeRegistry = nb.content.rendermime;
    }
}


/***/ }),

/***/ "./lib/extension/plugin.js":
/*!*********************************!*\
  !*** ./lib/extension/plugin.js ***!
  \*********************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   "plugin": () => (/* binding */ plugin)
/* harmony export */ });
/* harmony import */ var _jupyterlab_notebook__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! @jupyterlab/notebook */ "webpack/sharing/consume/default/@jupyterlab/notebook");
/* harmony import */ var _jupyterlab_notebook__WEBPACK_IMPORTED_MODULE_0___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_notebook__WEBPACK_IMPORTED_MODULE_0__);
/* harmony import */ var _utils__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! ../utils */ "./lib/utils/logging.js");
/* harmony import */ var _nbExtension__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! ./nbExtension */ "./lib/extension/nbExtension.js");



/**
 * Plugin initializes here
 */
const plugin = {
    id: 'interactivede:plugin',
    autoStart: true,
    requires: [_jupyterlab_notebook__WEBPACK_IMPORTED_MODULE_0__.INotebookTracker],
    activate // This is called to activate the plugin
};
function activate(app, nbTracker) {
    _utils__WEBPACK_IMPORTED_MODULE_1__.LOG.log('JupyterLab extension interactivede is activated!');
    console.log('JupyterLab extension interactivede is activated!');
    // Instantiate the widget extension which does the setup
    app.docRegistry.addWidgetExtension('notebook', new _nbExtension__WEBPACK_IMPORTED_MODULE_2__.NBWidgetExtension(nbTracker));
}


/***/ }),

/***/ "./lib/index.js":
/*!**********************!*\
  !*** ./lib/index.js ***!
  \**********************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   "default": () => (__WEBPACK_DEFAULT_EXPORT__)
/* harmony export */ });
/* harmony import */ var _extension__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! ./extension */ "./lib/extension/plugin.js");
/* harmony import */ var _extension__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! ./extension */ "./lib/extension/cellFactoryPlugin.js");

/* harmony default export */ const __WEBPACK_DEFAULT_EXPORT__ = ([_extension__WEBPACK_IMPORTED_MODULE_0__.plugin, _extension__WEBPACK_IMPORTED_MODULE_1__.cellFactoryPlugin]);


/***/ }),

/***/ "./lib/notebook/kernel/exec.js":
/*!*************************************!*\
  !*** ./lib/notebook/kernel/exec.js ***!
  \*************************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   "Executor": () => (/* binding */ Executor),
/* harmony export */   "PY_PD_TYPE": () => (/* binding */ PY_PD_TYPE),
/* harmony export */   "PY_STR_TYPE": () => (/* binding */ PY_STR_TYPE),
/* harmony export */   "Private": () => (/* binding */ Private)
/* harmony export */ });
/* harmony import */ var _lumino_signaling__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! @lumino/signaling */ "webpack/sharing/consume/default/@lumino/signaling");
/* harmony import */ var _lumino_signaling__WEBPACK_IMPORTED_MODULE_0___default = /*#__PURE__*/__webpack_require__.n(_lumino_signaling__WEBPACK_IMPORTED_MODULE_0__);
/* harmony import */ var _utils__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! ../../utils */ "./lib/utils/IDEGlobal.js");


const PY_STR_TYPE = 'str';
const PY_PD_TYPE = 'pandas.core.frame.DataFrame';
class Executor {
    constructor(nbPanel) {
        this._output = null;
        this._relayOutput = new _lumino_signaling__WEBPACK_IMPORTED_MODULE_0__.Signal(this);
        this._future = null;
        this._onIOPub = (msg) => {
            const msgType = msg.header.msg_type;
            switch (msgType) {
                case 'execute_result':
                case 'display_data':
                case 'update_display_data':
                    this._output = msg.content;
                    this._relayOutput.emit();
                    break;
                default:
                    break;
            }
        };
        this._ctx = nbPanel.sessionContext;
    }
    static init(nbTracker) {
        nbTracker.currentChanged.connect(async (_, nbPanel) => {
            if (!nbPanel)
                _utils__WEBPACK_IMPORTED_MODULE_1__.IDEGlobal.executor = null;
            else
                _utils__WEBPACK_IMPORTED_MODULE_1__.IDEGlobal.executor = new Executor(nbPanel);
        });
    }
    get hasFuture() {
        return Boolean(this._future);
    }
    get future() {
        if (!this._future)
            throw new Error('No future set');
        return this._future;
    }
    set future(val) {
        this._future = val;
        if (!val) {
            return;
        }
        val.onIOPub = this._onIOPub;
    }
    get output() {
        return this._output;
    }
    execute(code, { withIDE = false, withPandas = false, withJson = false } = {}) {
        var _a;
        if (withJson) {
            code = Private.withJson(code);
        }
        if (withPandas) {
            code = Private.withPandas(code);
        }
        if (withIDE) {
            code = Private.withIDE(code);
        }
        const kernel = (_a = this._ctx.session) === null || _a === void 0 ? void 0 : _a.kernel;
        if (!kernel) {
            return;
        }
        this.future = kernel.requestExecute({
            code,
            stop_on_error: true,
            store_history: false
        });
        return this.future;
    }
}
var Private;
(function (Private) {
    function withIDE(code) {
        return `from interactivede.internal import *\n${code}`;
    }
    Private.withIDE = withIDE;
    function withJson(code) {
        return `import json\n${code}`;
    }
    Private.withJson = withJson;
    function withPandas(code) {
        return `import pandas as pd\n${code}`;
    }
    Private.withPandas = withPandas;
})(Private || (Private = {}));


/***/ }),

/***/ "./lib/renderers/trrackGraphRenderer.js":
/*!**********************************************!*\
  !*** ./lib/renderers/trrackGraphRenderer.js ***!
  \**********************************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   "RenderedTrrackGraph": () => (/* binding */ RenderedTrrackGraph)
/* harmony export */ });
/* harmony import */ var _jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! @jupyterlab/apputils */ "webpack/sharing/consume/default/@jupyterlab/apputils");
/* harmony import */ var _jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_0___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_0__);
/* harmony import */ var _jupyterlab_rendermime__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! @jupyterlab/rendermime */ "webpack/sharing/consume/default/@jupyterlab/rendermime");
/* harmony import */ var _jupyterlab_rendermime__WEBPACK_IMPORTED_MODULE_1___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_rendermime__WEBPACK_IMPORTED_MODULE_1__);
/* harmony import */ var _lumino_widgets__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! @lumino/widgets */ "webpack/sharing/consume/default/@lumino/widgets");
/* harmony import */ var _lumino_widgets__WEBPACK_IMPORTED_MODULE_2___default = /*#__PURE__*/__webpack_require__.n(_lumino_widgets__WEBPACK_IMPORTED_MODULE_2__);
/* harmony import */ var react__WEBPACK_IMPORTED_MODULE_3__ = __webpack_require__(/*! react */ "webpack/sharing/consume/default/react");
/* harmony import */ var react__WEBPACK_IMPORTED_MODULE_3___default = /*#__PURE__*/__webpack_require__.n(react__WEBPACK_IMPORTED_MODULE_3__);
/* harmony import */ var _cells__WEBPACK_IMPORTED_MODULE_5__ = __webpack_require__(/*! ../cells */ "./lib/cells/TrrackVisComponent.js");
/* harmony import */ var _constants__WEBPACK_IMPORTED_MODULE_6__ = __webpack_require__(/*! ../constants */ "./lib/constants.js");
/* harmony import */ var _utils__WEBPACK_IMPORTED_MODULE_4__ = __webpack_require__(/*! ../utils */ "./lib/utils/IDEGlobal.js");







const TRRACK_VIS_HIDE_CLASS = 'jp-TrrackVisWidget-hide';
class TrrackVisWidget extends _jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_0__.ReactWidget {
    constructor(id) {
        super();
        const _tManager = _utils__WEBPACK_IMPORTED_MODULE_4__.IDEGlobal.trracks.get(id);
        if (!_tManager)
            throw new Error('TrrackManager not found');
        this._tManager = _tManager;
        this._hasVegaPlot = Boolean(_utils__WEBPACK_IMPORTED_MODULE_4__.IDEGlobal.views.get(id));
        this.toggle(this._hasVegaPlot);
    }
    toggle(to) {
        this.toggleClass(TRRACK_VIS_HIDE_CLASS, !to);
    }
    render() {
        return react__WEBPACK_IMPORTED_MODULE_3___default().createElement(_cells__WEBPACK_IMPORTED_MODULE_5__.TrrackVisComponent, { manager: this._tManager });
    }
}
class RenderedTrrackGraph extends _jupyterlab_rendermime__WEBPACK_IMPORTED_MODULE_1__.RenderedCommon {
    constructor(_options) {
        super(_options);
        this.layout = this._panelLayout = new _lumino_widgets__WEBPACK_IMPORTED_MODULE_2__.PanelLayout();
    }
    render(model) {
        const id = model.data[_constants__WEBPACK_IMPORTED_MODULE_6__.TRRACK_GRAPH_MIME_TYPE];
        const widget = new TrrackVisWidget(id);
        this._panelLayout.addWidget(widget);
        return Promise.resolve();
    }
}


/***/ }),

/***/ "./lib/renderers/trrackOutputRenderer.js":
/*!***********************************************!*\
  !*** ./lib/renderers/trrackOutputRenderer.js ***!
  \***********************************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   "RenderedTrrackOutput": () => (/* binding */ RenderedTrrackOutput)
/* harmony export */ });
/* harmony import */ var _jupyterlab_rendermime__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! @jupyterlab/rendermime */ "webpack/sharing/consume/default/@jupyterlab/rendermime");
/* harmony import */ var _jupyterlab_rendermime__WEBPACK_IMPORTED_MODULE_0___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_rendermime__WEBPACK_IMPORTED_MODULE_0__);
/* harmony import */ var _lumino_coreutils__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! @lumino/coreutils */ "webpack/sharing/consume/default/@lumino/coreutils");
/* harmony import */ var _lumino_coreutils__WEBPACK_IMPORTED_MODULE_1___default = /*#__PURE__*/__webpack_require__.n(_lumino_coreutils__WEBPACK_IMPORTED_MODULE_1__);
/* harmony import */ var _lumino_widgets__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! @lumino/widgets */ "webpack/sharing/consume/default/@lumino/widgets");
/* harmony import */ var _lumino_widgets__WEBPACK_IMPORTED_MODULE_2___default = /*#__PURE__*/__webpack_require__.n(_lumino_widgets__WEBPACK_IMPORTED_MODULE_2__);
/* harmony import */ var _constants__WEBPACK_IMPORTED_MODULE_4__ = __webpack_require__(/*! ../constants */ "./lib/constants.js");
/* harmony import */ var _utils__WEBPACK_IMPORTED_MODULE_3__ = __webpack_require__(/*! ../utils */ "./lib/utils/IDEGlobal.js");





const TRRACK_OUTPUT_AREA_OUTPUT_CLASS = 'trrack-OutputArea-output';
const TRRACK_OUTPUT_AREA_EXECUTE_RESULT_CLASS = 'trrack-OutputArea-executeResult';
const TRRACK_OUTPUT_AREA_ORIGINAL_CLASS = 'jp-OutputArea-output';
const TRRACK_OUTPUT_AREA_TRRACK_CLASS = 'trrack-OutputArea-trrack';
const ENABLE_SCROLL = 'enable-scroll';
const TRRACK_SECTION_ID = 'trrack';
const REGULAR_SECTION_ID = 'regular';
class RenderedTrrackOutput extends _jupyterlab_rendermime__WEBPACK_IMPORTED_MODULE_0__.RenderedCommon {
    constructor(_options) {
        super(_options);
        this._trrackCurrentId = '';
        this._currentRenderedData = '';
        this.addClass('lm-Panel');
        this.layout = this._panelLayout = new _lumino_widgets__WEBPACK_IMPORTED_MODULE_2__.PanelLayout();
        this.addClass(TRRACK_OUTPUT_AREA_OUTPUT_CLASS);
        this._regularOutputWidget = new _lumino_widgets__WEBPACK_IMPORTED_MODULE_2__.Panel();
        this._trrackOutputWidget = new _lumino_widgets__WEBPACK_IMPORTED_MODULE_2__.Panel();
        this._regularOutputWidget.id = REGULAR_SECTION_ID;
        this._trrackOutputWidget.id = TRRACK_SECTION_ID;
        this._regularOutputWidget.addClass(TRRACK_OUTPUT_AREA_EXECUTE_RESULT_CLASS);
        this._regularOutputWidget.addClass(TRRACK_OUTPUT_AREA_ORIGINAL_CLASS);
        this._panelLayout.addWidget(this._regularOutputWidget);
        this._trrackOutputWidget.addClass(TRRACK_OUTPUT_AREA_TRRACK_CLASS);
        this._panelLayout.addWidget(this._trrackOutputWidget);
    }
    async renderModel(model) {
        // Empty any existing content in the node from previous renders
        // while (this._panelLayout.widgets.length > 0) {
        //   this._panelLayout.widgets[0].dispose();
        //   this._panelLayout.removeWidgetAt(0);
        // }
        // while (this.node.firstChild) {
        //   this.node.removeChild(this.node.firstChild);
        // }
        // this._regularOutputWidget = new Panel();
        // this._regularOutputWidget.addClass(TRRACK_OUTPUT_AREA_EXECUTE_RESULT_CLASS);
        // this._regularOutputWidget.addClass(TRRACK_OUTPUT_AREA_ORIGINAL_CLASS);
        // this._panelLayout.addWidget(this._regularOutputWidget);
        // this._trrackOutputWidget = new Panel();
        // this._trrackOutputWidget.addClass(TRRACK_OUTPUT_AREA_TRRACK_CLASS);
        // this._panelLayout.addWidget(this._trrackOutputWidget);
        // Toggle the trusted class on the widget.
        this.toggleClass('jp-mod-trusted', model.trusted);
        // Render the actual content.
        await this.render(model);
        // Handle the fragment identifier if given.
        const { fragment } = model.metadata || {};
        if (fragment) {
            this.setFragment(fragment);
        }
    }
    async render(model) {
        var _a, _b;
        const { renderMimeRegistry } = _utils__WEBPACK_IMPORTED_MODULE_3__.IDEGlobal;
        const dataTypes = model.data[_constants__WEBPACK_IMPORTED_MODULE_4__.TRRACK_MIME_TYPE];
        if (!dataTypes)
            return Promise.resolve();
        const { [_constants__WEBPACK_IMPORTED_MODULE_4__.TRRACK_GRAPH_MIME_TYPE]: _id, ...data } = dataTypes;
        const id = _id;
        const renderPromises = [];
        if (id) {
            const trrackManager = _utils__WEBPACK_IMPORTED_MODULE_3__.IDEGlobal.trracks.get(id);
            if (this._trrackCurrentId !== (trrackManager === null || trrackManager === void 0 ? void 0 : trrackManager.current)) {
                this._trrackCurrentId = (trrackManager === null || trrackManager === void 0 ? void 0 : trrackManager.current) || '';
                while (this._trrackOutputWidget.widgets.length > 0) {
                    (_a = this._trrackOutputWidget.layout) === null || _a === void 0 ? void 0 : _a.widgets[0].dispose();
                    (_b = this._trrackOutputWidget.layout) === null || _b === void 0 ? void 0 : _b.removeWidgetAt(0);
                }
                const subModel = {
                    ...model,
                    metadata: model.metadata || {},
                    data: { [_constants__WEBPACK_IMPORTED_MODULE_4__.TRRACK_GRAPH_MIME_TYPE]: id }
                };
                const renderer = renderMimeRegistry.createRenderer(_constants__WEBPACK_IMPORTED_MODULE_4__.TRRACK_GRAPH_MIME_TYPE);
                const trrackPromise = renderer.renderModel(subModel).then(() => {
                    this._trrackOutputWidget.addWidget(renderer);
                });
                renderPromises.push(trrackPromise);
            }
        }
        if (data) {
            if (this._currentRenderedData !== JSON.stringify(data)) {
                this._currentRenderedData = JSON.stringify(data);
                const prefferedMimeType = renderMimeRegistry.preferredMimeType(data);
                if (!prefferedMimeType)
                    return Promise.resolve();
                const { [prefferedMimeType]: _data } = data;
                if (!_data)
                    return Promise.resolve();
                const subModel = {
                    trusted: model.trusted,
                    metadata: {
                        ...(model.metadata || {}),
                        cellId: id
                    },
                    data: {
                        [prefferedMimeType]: _data
                    },
                    setData(_options) {
                        return;
                    }
                };
                const renderer = renderMimeRegistry.createRenderer(prefferedMimeType);
                renderer.id = _lumino_coreutils__WEBPACK_IMPORTED_MODULE_1__.UUID.uuid4();
                // console.log('Set', renderer.id);
                const dataRender = renderer.renderModel(subModel).then(() => {
                    renderer.addClass(ENABLE_SCROLL);
                    this._regularOutputWidget.addWidget(renderer);
                    this._regularOutputWidget.widgets.forEach(w => {
                        var _a;
                        if (w.id !== renderer.id) {
                            (_a = this._regularOutputWidget.layout) === null || _a === void 0 ? void 0 : _a.removeWidget(w);
                        }
                    });
                });
                renderPromises.push(dataRender);
            }
        }
        return Promise.all(renderPromises).then(() => {
            var _a;
            (_a = _utils__WEBPACK_IMPORTED_MODULE_3__.IDEGlobal.cells.get(id)) === null || _a === void 0 ? void 0 : _a.addOutputWidget(this._panelLayout);
        });
    }
}


/***/ }),

/***/ "./lib/renderers/vegaRenderer.js":
/*!***************************************!*\
  !*** ./lib/renderers/vegaRenderer.js ***!
  \***************************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   "RenderedVega2": () => (/* binding */ RenderedVega2),
/* harmony export */   "getSpecFromModel": () => (/* binding */ getSpecFromModel)
/* harmony export */ });
/* harmony import */ var _jupyterlab_rendermime__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! @jupyterlab/rendermime */ "webpack/sharing/consume/default/@jupyterlab/rendermime");
/* harmony import */ var _jupyterlab_rendermime__WEBPACK_IMPORTED_MODULE_0___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_rendermime__WEBPACK_IMPORTED_MODULE_0__);
/* harmony import */ var _jupyterlab_vega5_extension__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! @jupyterlab/vega5-extension */ "webpack/sharing/consume/default/@jupyterlab/vega5-extension");
/* harmony import */ var _jupyterlab_vega5_extension__WEBPACK_IMPORTED_MODULE_1___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_vega5_extension__WEBPACK_IMPORTED_MODULE_1__);
/* harmony import */ var _lumino_widgets__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! @lumino/widgets */ "webpack/sharing/consume/default/@lumino/widgets");
/* harmony import */ var _lumino_widgets__WEBPACK_IMPORTED_MODULE_2___default = /*#__PURE__*/__webpack_require__.n(_lumino_widgets__WEBPACK_IMPORTED_MODULE_2__);
/* harmony import */ var _cells__WEBPACK_IMPORTED_MODULE_3__ = __webpack_require__(/*! ../cells */ "./lib/cells/trrack/vega/vegaManager.js");




class RenderedVega2 extends _jupyterlab_rendermime__WEBPACK_IMPORTED_MODULE_0__.RenderedCommon {
    constructor(options) {
        super(options);
        this._vegaManager = null;
        this.renderedVega = null;
        this.panelLayout = new _lumino_widgets__WEBPACK_IMPORTED_MODULE_2__.PanelLayout();
        this.widgetA = new _lumino_widgets__WEBPACK_IMPORTED_MODULE_2__.Panel();
        this.widgetB = new _lumino_widgets__WEBPACK_IMPORTED_MODULE_2__.Panel();
        this.currentVisible = 'A';
        this.opts = options;
        this.addClass('vega-parent');
        this.widgetA.addClass('vega-child');
        this.widgetB.addClass('vega-child');
        this.panelLayout.addWidget(this.widgetA);
        this.panelLayout.addWidget(this.widgetB);
        this.currentVisible === 'A' ? this.widgetB.hide() : this.widgetA.hide();
        this.layout = this.panelLayout;
    }
    get mimetype() {
        return 'application/vnd.vegalite.v4+json';
    }
    get vega() {
        var _a;
        return (_a = this.renderedVega) === null || _a === void 0 ? void 0 : _a._result;
    }
    async renderModel(model) {
        await this.render(model);
    }
    async render(model) {
        var _a;
        const cellId = model.metadata['cellId'];
        if (!cellId)
            throw new Error('No cellId found');
        this._vegaManager = _cells__WEBPACK_IMPORTED_MODULE_3__.VegaManager.init(cellId, this, getSpecFromModel(model));
        this.renderedVega = new _jupyterlab_vega5_extension__WEBPACK_IMPORTED_MODULE_1__.RenderedVega(this.opts);
        await this.renderedVega.renderModel(model);
        if (this.currentVisible === 'A') {
            while (this.widgetB.widgets.length > 0) {
                this.widgetB.layout.widgets[0].dispose();
                this.widgetB.layout.removeWidgetAt(0);
            }
            this.widgetB.node.textContent = '';
            this.widgetB.addWidget(this.renderedVega);
            this.widgetB.show();
            this.widgetA.hide();
            this.currentVisible = 'B';
        }
        else {
            while (this.widgetB.widgets.length > 0) {
                this.widgetB.layout.widgets[0].dispose();
                this.widgetB.layout.removeWidgetAt(0);
            }
            this.widgetA.node.textContent = '';
            this.widgetA.addWidget(this.renderedVega);
            this.widgetA.show();
            this.widgetB.hide();
            this.currentVisible = 'A';
        }
        if (RenderedVega2.previousRenderedVega) {
            RenderedVega2.previousRenderedVega.dispose();
        }
        RenderedVega2.previousRenderedVega = this.renderedVega;
        (_a = this._vegaManager) === null || _a === void 0 ? void 0 : _a.addListeners();
        return Promise.resolve();
    }
    dispose() {
        var _a;
        (_a = this._vegaManager) === null || _a === void 0 ? void 0 : _a.dispose();
        super.dispose();
    }
}
RenderedVega2.previousRenderedVega = null;
function getSpecFromModel(model) {
    const mimeType = Object.keys((model === null || model === void 0 ? void 0 : model.data) || {}).find(m => m.includes('vegalite') && m.includes('v4'));
    if (!mimeType)
        throw new Error('No vegalite4 spec');
    const spec = model === null || model === void 0 ? void 0 : model.data[mimeType];
    if (!spec)
        throw new Error('No vegalite4 spec');
    return spec;
}


/***/ }),

/***/ "./lib/utils/IDEGlobal.js":
/*!********************************!*\
  !*** ./lib/utils/IDEGlobal.js ***!
  \********************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   "IDEGlobal": () => (/* binding */ IDEGlobal)
/* harmony export */ });
// eslint-disable-next-line @typescript-eslint/naming-convention
class IDEGlobal {
}
window.IDEGlobal = IDEGlobal;


/***/ }),

/***/ "./lib/utils/debounce.js":
/*!*******************************!*\
  !*** ./lib/utils/debounce.js ***!
  \*******************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   "debounce": () => (/* binding */ debounce)
/* harmony export */ });
function debounce(func, wait = 300) {
    let timeout;
    return (...args) => {
        clearTimeout(timeout);
        timeout = setTimeout(() => func(...args), wait);
    };
}


/***/ }),

/***/ "./lib/utils/disposable.js":
/*!*********************************!*\
  !*** ./lib/utils/disposable.js ***!
  \*********************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   "Disposable": () => (/* binding */ Disposable)
/* harmony export */ });
class Disposable {
    constructor() {
        this._isDisposed = false;
    }
    get isDisposed() {
        return this._isDisposed;
    }
    set isDisposed(value) {
        this._isDisposed = value;
    }
}


/***/ }),

/***/ "./lib/utils/logging.js":
/*!******************************!*\
  !*** ./lib/utils/logging.js ***!
  \******************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   "LOG": () => (/* binding */ LOG)
/* harmony export */ });
/* harmony import */ var _IDEGlobal__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! ./IDEGlobal */ "./lib/utils/IDEGlobal.js");

function init() {
    const events = [];
    let notebook = null;
    let timer = null;
    setInterval(() => {
        save();
    }, 5000);
    function log(name, data) {
        if (data)
            events.push({ name, date: new Date(), data });
        else
            events.push({ name, date: new Date() });
    }
    function print(asTable = true) {
        if (asTable)
            console.table(events);
        else
            console.log({
                logEvents: events
            });
    }
    function setNotebook(nb) {
        notebook = nb;
    }
    function save() {
        var _a;
        (_a = notebook === null || notebook === void 0 ? void 0 : notebook.model) === null || _a === void 0 ? void 0 : _a.metadata.set('ext-ide-logs', events);
    }
    function autoSave(enable = 5000) {
        if (timer) {
            clearInterval(timer);
        }
        if (typeof enable === 'number') {
            timer = setInterval(() => {
                save();
            }, enable);
        }
    }
    return {
        log,
        print,
        setNotebook,
        save,
        autoSave
    };
}
const LOG = init();
_IDEGlobal__WEBPACK_IMPORTED_MODULE_0__.IDEGlobal.LOGGER = LOG;
LOG.log('logging initialized');
LOG.save();


/***/ })

}]);
//# sourceMappingURL=lib_index_js.affd35e8f9a79986cc4d.js.map