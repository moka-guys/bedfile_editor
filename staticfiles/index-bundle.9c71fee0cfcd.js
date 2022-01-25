/*
 * ATTENTION: The "eval" devtool has been used (maybe by default in mode: "development").
 * This devtool is neither made for production nor for readable output files.
 * It uses "eval()" calls to create a separate source file in the browser devtools.
 * If you are trying to read the output file, select a different devtool (https://webpack.js.org/configuration/devtool/)
 * or disable the default devtool with "devtool: false".
 * If you are looking for production-ready output files, see mode: "production" (https://webpack.js.org/configuration/mode/).
 */
/******/ (() => { // webpackBootstrap
/******/ 	"use strict";
/******/ 	var __webpack_modules__ = ({

/***/ "./assets/index.js":
/*!*************************!*\
  !*** ./assets/index.js ***!
  \*************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

eval("__webpack_require__.r(__webpack_exports__);\n\n\nfunction component() {\n  //define data array\n  var tabledata = [{\n    id: 1,\n    name: \"Oli Bob\",\n    progress: 12,\n    gender: \"male\",\n    rating: 1,\n    col: \"red\",\n    dob: \"19/02/1984\",\n    car: 1\n  }, {\n    id: 2,\n    name: \"Mary May\",\n    progress: 1,\n    gender: \"female\",\n    rating: 2,\n    col: \"blue\",\n    dob: \"14/05/1982\",\n    car: true\n  }, {\n    id: 3,\n    name: \"Christine Lobowski\",\n    progress: 42,\n    gender: \"female\",\n    rating: 0,\n    col: \"green\",\n    dob: \"22/05/1982\",\n    car: \"true\"\n  }, {\n    id: 4,\n    name: \"Brendon Philips\",\n    progress: 100,\n    gender: \"male\",\n    rating: 1,\n    col: \"orange\",\n    dob: \"01/08/1980\"\n  }, {\n    id: 5,\n    name: \"Margret Marmajuke\",\n    progress: 16,\n    gender: \"female\",\n    rating: 5,\n    col: \"yellow\",\n    dob: \"31/01/1999\"\n  }, {\n    id: 6,\n    name: \"Frank Harbours\",\n    progress: 38,\n    gender: \"male\",\n    rating: 4,\n    col: \"red\",\n    dob: \"12/05/1966\",\n    car: 1\n  }]; //initialize table\n\n  var table = new Tabulator(\"#example-table\", {\n    data: tabledata,\n    //assign data to table\n    autoColumns: true //create columns from data field names\n\n  });\n}\n\ndocument.body.appendChild(component());\n\n//# sourceURL=webpack://bedfile_editor/./assets/index.js?");

/***/ })

/******/ 	});
/************************************************************************/
/******/ 	// The require scope
/******/ 	var __webpack_require__ = {};
/******/ 	
/************************************************************************/
/******/ 	/* webpack/runtime/make namespace object */
/******/ 	(() => {
/******/ 		// define __esModule on exports
/******/ 		__webpack_require__.r = (exports) => {
/******/ 			if(typeof Symbol !== 'undefined' && Symbol.toStringTag) {
/******/ 				Object.defineProperty(exports, Symbol.toStringTag, { value: 'Module' });
/******/ 			}
/******/ 			Object.defineProperty(exports, '__esModule', { value: true });
/******/ 		};
/******/ 	})();
/******/ 	
/************************************************************************/
/******/ 	
/******/ 	// startup
/******/ 	// Load entry module and return exports
/******/ 	// This entry module can't be inlined because the eval devtool is used.
/******/ 	var __webpack_exports__ = {};
/******/ 	__webpack_modules__["./assets/index.js"](0, __webpack_exports__, __webpack_require__);
/******/ 	
/******/ })()
;