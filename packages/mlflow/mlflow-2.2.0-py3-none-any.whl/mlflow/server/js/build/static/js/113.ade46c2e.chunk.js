"use strict";(self.webpackChunk_mlflow_mlflow=self.webpackChunk_mlflow_mlflow||[]).push([[113],{13002:function(e,t,r){r.r(t),r.d(t,{SKELETON_TYPE:function(){return h},TYPE:function(){return n},createLiteralElement:function(){return H},createNumberElement:function(){return m},isArgumentElement:function(){return a},isDateElement:function(){return l},isDateTimeSkeleton:function(){return _},isLiteralElement:function(){return o},isNumberElement:function(){return u},isNumberSkeleton:function(){return g},isPluralElement:function(){return p},isPoundElement:function(){return f},isSelectElement:function(){return E},isTagElement:function(){return b},isTimeElement:function(){return c},parse:function(){return oe}});var i,n,h,s=r(21448);function o(e){return e.type===n.literal}function a(e){return e.type===n.argument}function u(e){return e.type===n.number}function l(e){return e.type===n.date}function c(e){return e.type===n.time}function E(e){return e.type===n.select}function p(e){return e.type===n.plural}function f(e){return e.type===n.pound}function b(e){return e.type===n.tag}function g(e){return!(!e||"object"!==typeof e||e.type!==h.number)}function _(e){return!(!e||"object"!==typeof e||e.type!==h.dateTime)}function H(e){return{type:n.literal,value:e}}function m(e,t){return{type:n.number,value:e,style:t}}!function(e){e[e.EXPECT_ARGUMENT_CLOSING_BRACE=1]="EXPECT_ARGUMENT_CLOSING_BRACE",e[e.EMPTY_ARGUMENT=2]="EMPTY_ARGUMENT",e[e.MALFORMED_ARGUMENT=3]="MALFORMED_ARGUMENT",e[e.EXPECT_ARGUMENT_TYPE=4]="EXPECT_ARGUMENT_TYPE",e[e.INVALID_ARGUMENT_TYPE=5]="INVALID_ARGUMENT_TYPE",e[e.EXPECT_ARGUMENT_STYLE=6]="EXPECT_ARGUMENT_STYLE",e[e.INVALID_NUMBER_SKELETON=7]="INVALID_NUMBER_SKELETON",e[e.INVALID_DATE_TIME_SKELETON=8]="INVALID_DATE_TIME_SKELETON",e[e.EXPECT_NUMBER_SKELETON=9]="EXPECT_NUMBER_SKELETON",e[e.EXPECT_DATE_TIME_SKELETON=10]="EXPECT_DATE_TIME_SKELETON",e[e.UNCLOSED_QUOTE_IN_ARGUMENT_STYLE=11]="UNCLOSED_QUOTE_IN_ARGUMENT_STYLE",e[e.EXPECT_SELECT_ARGUMENT_OPTIONS=12]="EXPECT_SELECT_ARGUMENT_OPTIONS",e[e.EXPECT_PLURAL_ARGUMENT_OFFSET_VALUE=13]="EXPECT_PLURAL_ARGUMENT_OFFSET_VALUE",e[e.INVALID_PLURAL_ARGUMENT_OFFSET_VALUE=14]="INVALID_PLURAL_ARGUMENT_OFFSET_VALUE",e[e.EXPECT_SELECT_ARGUMENT_SELECTOR=15]="EXPECT_SELECT_ARGUMENT_SELECTOR",e[e.EXPECT_PLURAL_ARGUMENT_SELECTOR=16]="EXPECT_PLURAL_ARGUMENT_SELECTOR",e[e.EXPECT_SELECT_ARGUMENT_SELECTOR_FRAGMENT=17]="EXPECT_SELECT_ARGUMENT_SELECTOR_FRAGMENT",e[e.EXPECT_PLURAL_ARGUMENT_SELECTOR_FRAGMENT=18]="EXPECT_PLURAL_ARGUMENT_SELECTOR_FRAGMENT",e[e.INVALID_PLURAL_ARGUMENT_SELECTOR=19]="INVALID_PLURAL_ARGUMENT_SELECTOR",e[e.DUPLICATE_PLURAL_ARGUMENT_SELECTOR=20]="DUPLICATE_PLURAL_ARGUMENT_SELECTOR",e[e.DUPLICATE_SELECT_ARGUMENT_SELECTOR=21]="DUPLICATE_SELECT_ARGUMENT_SELECTOR",e[e.MISSING_OTHER_CLAUSE=22]="MISSING_OTHER_CLAUSE",e[e.INVALID_TAG=23]="INVALID_TAG",e[e.INVALID_TAG_NAME=25]="INVALID_TAG_NAME",e[e.UNMATCHED_CLOSING_TAG=26]="UNMATCHED_CLOSING_TAG",e[e.UNCLOSED_TAG=27]="UNCLOSED_TAG"}(i||(i={})),function(e){e[e.literal=0]="literal",e[e.argument=1]="argument",e[e.number=2]="number",e[e.date=3]="date",e[e.time=4]="time",e[e.select=5]="select",e[e.plural=6]="plural",e[e.pound=7]="pound",e[e.tag=8]="tag"}(n||(n={})),function(e){e[e.number=0]="number",e[e.dateTime=1]="dateTime"}(h||(h={}));var B=/[ \xA0\u1680\u2000-\u200A\u202F\u205F\u3000]/,T=/(?:[Eec]{1,6}|G{1,5}|[Qq]{1,5}|(?:[yYur]+|U{1,5})|[ML]{1,5}|d{1,2}|D{1,3}|F{1}|[abB]{1,5}|[hkHK]{1,2}|w{1,2}|W{1}|m{1,2}|s{1,2}|[zZOvVxX]{1,4})(?=([^']*'[^']*')*[^']*$)/g;function S(e){var t={};return e.replace(T,(function(e){var r=e.length;switch(e[0]){case"G":t.era=4===r?"long":5===r?"narrow":"short";break;case"y":t.year=2===r?"2-digit":"numeric";break;case"Y":case"u":case"U":case"r":throw new RangeError("`Y/u/U/r` (year) patterns are not supported, use `y` instead");case"q":case"Q":throw new RangeError("`q/Q` (quarter) patterns are not supported");case"M":case"L":t.month=["numeric","2-digit","short","long","narrow"][r-1];break;case"w":case"W":throw new RangeError("`w/W` (week) patterns are not supported");case"d":t.day=["numeric","2-digit"][r-1];break;case"D":case"F":case"g":throw new RangeError("`D/F/g` (day) patterns are not supported, use `d` instead");case"E":t.weekday=4===r?"short":5===r?"narrow":"short";break;case"e":if(r<4)throw new RangeError("`e..eee` (weekday) patterns are not supported");t.weekday=["short","long","narrow","short"][r-4];break;case"c":if(r<4)throw new RangeError("`c..ccc` (weekday) patterns are not supported");t.weekday=["short","long","narrow","short"][r-4];break;case"a":t.hour12=!0;break;case"b":case"B":throw new RangeError("`b/B` (period) patterns are not supported, use `a` instead");case"h":t.hourCycle="h12",t.hour=["numeric","2-digit"][r-1];break;case"H":t.hourCycle="h23",t.hour=["numeric","2-digit"][r-1];break;case"K":t.hourCycle="h11",t.hour=["numeric","2-digit"][r-1];break;case"k":t.hourCycle="h24",t.hour=["numeric","2-digit"][r-1];break;case"j":case"J":case"C":throw new RangeError("`j/J/C` (hour) patterns are not supported, use `h/H/K/k` instead");case"m":t.minute=["numeric","2-digit"][r-1];break;case"s":t.second=["numeric","2-digit"][r-1];break;case"S":case"A":throw new RangeError("`S/A` (second) patterns are not supported, use `s` instead");case"z":t.timeZoneName=r<4?"short":"long";break;case"Z":case"O":case"v":case"V":case"X":case"x":throw new RangeError("`Z/O/v/V/X/x` (timeZone) patterns are not supported, use `z` instead")}return""})),t}var A=/[\t-\r \x85\u200E\u200F\u2028\u2029]/i;var v=/^\.(?:(0+)(\*)?|(#+)|(0+)(#+))$/g,P=/^(@+)?(\+|#+)?[rs]?$/g,y=/(\*)(0+)|(#+)(0+)|(0+)/g,L=/^(0+)$/;function N(e){var t={};return"r"===e[e.length-1]?t.roundingPriority="morePrecision":"s"===e[e.length-1]&&(t.roundingPriority="lessPrecision"),e.replace(P,(function(e,r,i){return"string"!==typeof i?(t.minimumSignificantDigits=r.length,t.maximumSignificantDigits=r.length):"+"===i?t.minimumSignificantDigits=r.length:"#"===r[0]?t.maximumSignificantDigits=r.length:(t.minimumSignificantDigits=r.length,t.maximumSignificantDigits=r.length+("string"===typeof i?i.length:0)),""})),t}function C(e){switch(e){case"sign-auto":return{signDisplay:"auto"};case"sign-accounting":case"()":return{currencySign:"accounting"};case"sign-always":case"+!":return{signDisplay:"always"};case"sign-accounting-always":case"()!":return{signDisplay:"always",currencySign:"accounting"};case"sign-except-zero":case"+?":return{signDisplay:"exceptZero"};case"sign-accounting-except-zero":case"()?":return{signDisplay:"exceptZero",currencySign:"accounting"};case"sign-never":case"+_":return{signDisplay:"never"}}}function d(e){var t;if("E"===e[0]&&"E"===e[1]?(t={notation:"engineering"},e=e.slice(2)):"E"===e[0]&&(t={notation:"scientific"},e=e.slice(1)),t){var r=e.slice(0,2);if("+!"===r?(t.signDisplay="always",e=e.slice(2)):"+?"===r&&(t.signDisplay="exceptZero",e=e.slice(2)),!L.test(e))throw new Error("Malformed concise eng/scientific notation");t.minimumIntegerDigits=e.length}return t}function R(e){var t=C(e);return t||{}}function I(e){for(var t={},r=0,i=e;r<i.length;r++){var n=i[r];switch(n.stem){case"percent":case"%":t.style="percent";continue;case"%x100":t.style="percent",t.scale=100;continue;case"currency":t.style="currency",t.currency=n.options[0];continue;case"group-off":case",_":t.useGrouping=!1;continue;case"precision-integer":case".":t.maximumFractionDigits=0;continue;case"measure-unit":case"unit":t.style="unit",t.unit=n.options[0].replace(/^(.*?)-/,"");continue;case"compact-short":case"K":t.notation="compact",t.compactDisplay="short";continue;case"compact-long":case"KK":t.notation="compact",t.compactDisplay="long";continue;case"scientific":t=(0,s.__assign)((0,s.__assign)((0,s.__assign)({},t),{notation:"scientific"}),n.options.reduce((function(e,t){return(0,s.__assign)((0,s.__assign)({},e),R(t))}),{}));continue;case"engineering":t=(0,s.__assign)((0,s.__assign)((0,s.__assign)({},t),{notation:"engineering"}),n.options.reduce((function(e,t){return(0,s.__assign)((0,s.__assign)({},e),R(t))}),{}));continue;case"notation-simple":t.notation="standard";continue;case"unit-width-narrow":t.currencyDisplay="narrowSymbol",t.unitDisplay="narrow";continue;case"unit-width-short":t.currencyDisplay="code",t.unitDisplay="short";continue;case"unit-width-full-name":t.currencyDisplay="name",t.unitDisplay="long";continue;case"unit-width-iso-code":t.currencyDisplay="symbol";continue;case"scale":t.scale=parseFloat(n.options[0]);continue;case"integer-width":if(n.options.length>1)throw new RangeError("integer-width stems only accept a single optional option");n.options[0].replace(y,(function(e,r,i,n,h,s){if(r)t.minimumIntegerDigits=i.length;else{if(n&&h)throw new Error("We currently do not support maximum integer digits");if(s)throw new Error("We currently do not support exact integer digits")}return""}));continue}if(L.test(n.stem))t.minimumIntegerDigits=n.stem.length;else if(v.test(n.stem)){if(n.options.length>1)throw new RangeError("Fraction-precision stems only accept a single optional option");n.stem.replace(v,(function(e,r,i,n,h,s){return"*"===i?t.minimumFractionDigits=r.length:n&&"#"===n[0]?t.maximumFractionDigits=n.length:h&&s?(t.minimumFractionDigits=h.length,t.maximumFractionDigits=h.length+s.length):(t.minimumFractionDigits=r.length,t.maximumFractionDigits=r.length),""}));var h=n.options[0];"w"===h?t=(0,s.__assign)((0,s.__assign)({},t),{trailingZeroDisplay:"stripIfInteger"}):h&&(t=(0,s.__assign)((0,s.__assign)({},t),N(h)))}else if(P.test(n.stem))t=(0,s.__assign)((0,s.__assign)({},t),N(n.stem));else{var o=C(n.stem);o&&(t=(0,s.__assign)((0,s.__assign)({},t),o));var a=d(n.stem);a&&(t=(0,s.__assign)((0,s.__assign)({},t),a))}}return t}var M,U={AX:["H"],BQ:["H"],CP:["H"],CZ:["H"],DK:["H"],FI:["H"],ID:["H"],IS:["H"],ML:["H"],NE:["H"],RU:["H"],SE:["H"],SJ:["H"],SK:["H"],AS:["h","H"],BT:["h","H"],DJ:["h","H"],ER:["h","H"],GH:["h","H"],IN:["h","H"],LS:["h","H"],PG:["h","H"],PW:["h","H"],SO:["h","H"],TO:["h","H"],VU:["h","H"],WS:["h","H"],"001":["H","h"],AL:["h","H","hB"],TD:["h","H","hB"],"ca-ES":["H","h","hB"],CF:["H","h","hB"],CM:["H","h","hB"],"fr-CA":["H","h","hB"],"gl-ES":["H","h","hB"],"it-CH":["H","h","hB"],"it-IT":["H","h","hB"],LU:["H","h","hB"],NP:["H","h","hB"],PF:["H","h","hB"],SC:["H","h","hB"],SM:["H","h","hB"],SN:["H","h","hB"],TF:["H","h","hB"],VA:["H","h","hB"],CY:["h","H","hb","hB"],GR:["h","H","hb","hB"],CO:["h","H","hB","hb"],DO:["h","H","hB","hb"],KP:["h","H","hB","hb"],KR:["h","H","hB","hb"],NA:["h","H","hB","hb"],PA:["h","H","hB","hb"],PR:["h","H","hB","hb"],VE:["h","H","hB","hb"],AC:["H","h","hb","hB"],AI:["H","h","hb","hB"],BW:["H","h","hb","hB"],BZ:["H","h","hb","hB"],CC:["H","h","hb","hB"],CK:["H","h","hb","hB"],CX:["H","h","hb","hB"],DG:["H","h","hb","hB"],FK:["H","h","hb","hB"],GB:["H","h","hb","hB"],GG:["H","h","hb","hB"],GI:["H","h","hb","hB"],IE:["H","h","hb","hB"],IM:["H","h","hb","hB"],IO:["H","h","hb","hB"],JE:["H","h","hb","hB"],LT:["H","h","hb","hB"],MK:["H","h","hb","hB"],MN:["H","h","hb","hB"],MS:["H","h","hb","hB"],NF:["H","h","hb","hB"],NG:["H","h","hb","hB"],NR:["H","h","hb","hB"],NU:["H","h","hb","hB"],PN:["H","h","hb","hB"],SH:["H","h","hb","hB"],SX:["H","h","hb","hB"],TA:["H","h","hb","hB"],ZA:["H","h","hb","hB"],"af-ZA":["H","h","hB","hb"],AR:["H","h","hB","hb"],CL:["H","h","hB","hb"],CR:["H","h","hB","hb"],CU:["H","h","hB","hb"],EA:["H","h","hB","hb"],"es-BO":["H","h","hB","hb"],"es-BR":["H","h","hB","hb"],"es-EC":["H","h","hB","hb"],"es-ES":["H","h","hB","hb"],"es-GQ":["H","h","hB","hb"],"es-PE":["H","h","hB","hb"],GT:["H","h","hB","hb"],HN:["H","h","hB","hb"],IC:["H","h","hB","hb"],KG:["H","h","hB","hb"],KM:["H","h","hB","hb"],LK:["H","h","hB","hb"],MA:["H","h","hB","hb"],MX:["H","h","hB","hb"],NI:["H","h","hB","hb"],PY:["H","h","hB","hb"],SV:["H","h","hB","hb"],UY:["H","h","hB","hb"],JP:["H","h","K"],AD:["H","hB"],AM:["H","hB"],AO:["H","hB"],AT:["H","hB"],AW:["H","hB"],BE:["H","hB"],BF:["H","hB"],BJ:["H","hB"],BL:["H","hB"],BR:["H","hB"],CG:["H","hB"],CI:["H","hB"],CV:["H","hB"],DE:["H","hB"],EE:["H","hB"],FR:["H","hB"],GA:["H","hB"],GF:["H","hB"],GN:["H","hB"],GP:["H","hB"],GW:["H","hB"],HR:["H","hB"],IL:["H","hB"],IT:["H","hB"],KZ:["H","hB"],MC:["H","hB"],MD:["H","hB"],MF:["H","hB"],MQ:["H","hB"],MZ:["H","hB"],NC:["H","hB"],NL:["H","hB"],PM:["H","hB"],PT:["H","hB"],RE:["H","hB"],RO:["H","hB"],SI:["H","hB"],SR:["H","hB"],ST:["H","hB"],TG:["H","hB"],TR:["H","hB"],WF:["H","hB"],YT:["H","hB"],BD:["h","hB","H"],PK:["h","hB","H"],AZ:["H","hB","h"],BA:["H","hB","h"],BG:["H","hB","h"],CH:["H","hB","h"],GE:["H","hB","h"],LI:["H","hB","h"],ME:["H","hB","h"],RS:["H","hB","h"],UA:["H","hB","h"],UZ:["H","hB","h"],XK:["H","hB","h"],AG:["h","hb","H","hB"],AU:["h","hb","H","hB"],BB:["h","hb","H","hB"],BM:["h","hb","H","hB"],BS:["h","hb","H","hB"],CA:["h","hb","H","hB"],DM:["h","hb","H","hB"],"en-001":["h","hb","H","hB"],FJ:["h","hb","H","hB"],FM:["h","hb","H","hB"],GD:["h","hb","H","hB"],GM:["h","hb","H","hB"],GU:["h","hb","H","hB"],GY:["h","hb","H","hB"],JM:["h","hb","H","hB"],KI:["h","hb","H","hB"],KN:["h","hb","H","hB"],KY:["h","hb","H","hB"],LC:["h","hb","H","hB"],LR:["h","hb","H","hB"],MH:["h","hb","H","hB"],MP:["h","hb","H","hB"],MW:["h","hb","H","hB"],NZ:["h","hb","H","hB"],SB:["h","hb","H","hB"],SG:["h","hb","H","hB"],SL:["h","hb","H","hB"],SS:["h","hb","H","hB"],SZ:["h","hb","H","hB"],TC:["h","hb","H","hB"],TT:["h","hb","H","hB"],UM:["h","hb","H","hB"],US:["h","hb","H","hB"],VC:["h","hb","H","hB"],VG:["h","hb","H","hB"],VI:["h","hb","H","hB"],ZM:["h","hb","H","hB"],BO:["H","hB","h","hb"],EC:["H","hB","h","hb"],ES:["H","hB","h","hb"],GQ:["H","hB","h","hb"],PE:["H","hB","h","hb"],AE:["h","hB","hb","H"],"ar-001":["h","hB","hb","H"],BH:["h","hB","hb","H"],DZ:["h","hB","hb","H"],EG:["h","hB","hb","H"],EH:["h","hB","hb","H"],HK:["h","hB","hb","H"],IQ:["h","hB","hb","H"],JO:["h","hB","hb","H"],KW:["h","hB","hb","H"],LB:["h","hB","hb","H"],LY:["h","hB","hb","H"],MO:["h","hB","hb","H"],MR:["h","hB","hb","H"],OM:["h","hB","hb","H"],PH:["h","hB","hb","H"],PS:["h","hB","hb","H"],QA:["h","hB","hb","H"],SA:["h","hB","hb","H"],SD:["h","hB","hb","H"],SY:["h","hB","hb","H"],TN:["h","hB","hb","H"],YE:["h","hB","hb","H"],AF:["H","hb","hB","h"],LA:["H","hb","hB","h"],CN:["H","hB","hb","h"],LV:["H","hB","hb","h"],TL:["H","hB","hb","h"],"zu-ZA":["H","hB","hb","h"],CD:["hB","H"],IR:["hB","H"],"hi-IN":["hB","h","H"],"kn-IN":["hB","h","H"],"ml-IN":["hB","h","H"],"te-IN":["hB","h","H"],KH:["hB","h","H","hb"],"ta-IN":["hB","h","hb","H"],BN:["hb","hB","h","H"],MY:["hb","hB","h","H"],ET:["hB","hb","h","H"],"gu-IN":["hB","hb","h","H"],"mr-IN":["hB","hb","h","H"],"pa-IN":["hB","hb","h","H"],TW:["hB","hb","h","H"],KE:["hB","hb","H","h"],MM:["hB","hb","H","h"],TZ:["hB","hb","H","h"],UG:["hB","hb","H","h"]};function O(e){var t=e.hourCycle;if(void 0===t&&e.hourCycles&&e.hourCycles.length&&(t=e.hourCycles[0]),t)switch(t){case"h24":return"k";case"h23":return"H";case"h12":return"h";case"h11":return"K";default:throw new Error("Invalid hourCycle")}var r,i=e.language;return"root"!==i&&(r=e.maximize().region),(U[r||""]||U[i||""]||U["".concat(i,"-001")]||U["001"])[0]}var G=new RegExp("^".concat(B.source,"*")),D=new RegExp("".concat(B.source,"*$"));function w(e,t){return{start:e,end:t}}var F=!!String.prototype.startsWith,k=!!String.fromCodePoint,X=!!Object.fromEntries,V=!!String.prototype.codePointAt,K=!!String.prototype.trimStart,x=!!String.prototype.trimEnd,Y=!!Number.isSafeInteger?Number.isSafeInteger:function(e){return"number"===typeof e&&isFinite(e)&&Math.floor(e)===e&&Math.abs(e)<=9007199254740991},Z=!0;try{Z="a"===(null===(M=ee("([^\\p{White_Space}\\p{Pattern_Syntax}]*)","yu").exec("a"))||void 0===M?void 0:M[0])}catch(ae){Z=!1}var W,j=F?function(e,t,r){return e.startsWith(t,r)}:function(e,t,r){return e.slice(r,r+t.length)===t},Q=k?String.fromCodePoint:function(){for(var e=[],t=0;t<arguments.length;t++)e[t]=arguments[t];for(var r,i="",n=e.length,h=0;n>h;){if((r=e[h++])>1114111)throw RangeError(r+" is not a valid code point");i+=r<65536?String.fromCharCode(r):String.fromCharCode(55296+((r-=65536)>>10),r%1024+56320)}return i},q=X?Object.fromEntries:function(e){for(var t={},r=0,i=e;r<i.length;r++){var n=i[r],h=n[0],s=n[1];t[h]=s}return t},J=V?function(e,t){return e.codePointAt(t)}:function(e,t){var r=e.length;if(!(t<0||t>=r)){var i,n=e.charCodeAt(t);return n<55296||n>56319||t+1===r||(i=e.charCodeAt(t+1))<56320||i>57343?n:i-56320+(n-55296<<10)+65536}},z=K?function(e){return e.trimStart()}:function(e){return e.replace(G,"")},$=x?function(e){return e.trimEnd()}:function(e){return e.replace(D,"")};function ee(e,t){return new RegExp(e,t)}if(Z){var te=ee("([^\\p{White_Space}\\p{Pattern_Syntax}]*)","yu");W=function(e,t){var r;return te.lastIndex=t,null!==(r=te.exec(e)[1])&&void 0!==r?r:""}}else W=function(e,t){for(var r=[];;){var i=J(e,t);if(void 0===i||ne(i)||he(i))break;r.push(i),t+=i>=65536?2:1}return Q.apply(void 0,r)};var re=function(){function e(e,t){void 0===t&&(t={}),this.message=e,this.position={offset:0,line:1,column:1},this.ignoreTag=!!t.ignoreTag,this.locale=t.locale,this.requiresOtherClause=!!t.requiresOtherClause,this.shouldParseSkeletons=!!t.shouldParseSkeletons}return e.prototype.parse=function(){if(0!==this.offset())throw Error("parser can only be used once");return this.parseMessage(0,"",!1)},e.prototype.parseMessage=function(e,t,r){for(var h=[];!this.isEOF();){var s=this.char();if(123===s){if((o=this.parseArgument(e,r)).err)return o;h.push(o.val)}else{if(125===s&&e>0)break;if(35!==s||"plural"!==t&&"selectordinal"!==t){if(60===s&&!this.ignoreTag&&47===this.peek()){if(r)break;return this.error(i.UNMATCHED_CLOSING_TAG,w(this.clonePosition(),this.clonePosition()))}if(60===s&&!this.ignoreTag&&ie(this.peek()||0)){if((o=this.parseTag(e,t)).err)return o;h.push(o.val)}else{var o;if((o=this.parseLiteral(e,t)).err)return o;h.push(o.val)}}else{var a=this.clonePosition();this.bump(),h.push({type:n.pound,location:w(a,this.clonePosition())})}}}return{val:h,err:null}},e.prototype.parseTag=function(e,t){var r=this.clonePosition();this.bump();var h=this.parseTagName();if(this.bumpSpace(),this.bumpIf("/>"))return{val:{type:n.literal,value:"<".concat(h,"/>"),location:w(r,this.clonePosition())},err:null};if(this.bumpIf(">")){var s=this.parseMessage(e+1,t,!0);if(s.err)return s;var o=s.val,a=this.clonePosition();if(this.bumpIf("</")){if(this.isEOF()||!ie(this.char()))return this.error(i.INVALID_TAG,w(a,this.clonePosition()));var u=this.clonePosition();return h!==this.parseTagName()?this.error(i.UNMATCHED_CLOSING_TAG,w(u,this.clonePosition())):(this.bumpSpace(),this.bumpIf(">")?{val:{type:n.tag,value:h,children:o,location:w(r,this.clonePosition())},err:null}:this.error(i.INVALID_TAG,w(a,this.clonePosition())))}return this.error(i.UNCLOSED_TAG,w(r,this.clonePosition()))}return this.error(i.INVALID_TAG,w(r,this.clonePosition()))},e.prototype.parseTagName=function(){var e,t=this.offset();for(this.bump();!this.isEOF()&&(45===(e=this.char())||46===e||e>=48&&e<=57||95===e||e>=97&&e<=122||e>=65&&e<=90||183==e||e>=192&&e<=214||e>=216&&e<=246||e>=248&&e<=893||e>=895&&e<=8191||e>=8204&&e<=8205||e>=8255&&e<=8256||e>=8304&&e<=8591||e>=11264&&e<=12271||e>=12289&&e<=55295||e>=63744&&e<=64975||e>=65008&&e<=65533||e>=65536&&e<=983039);)this.bump();return this.message.slice(t,this.offset())},e.prototype.parseLiteral=function(e,t){for(var r=this.clonePosition(),i="";;){var h=this.tryParseQuote(t);if(h)i+=h;else{var s=this.tryParseUnquoted(e,t);if(s)i+=s;else{var o=this.tryParseLeftAngleBracket();if(!o)break;i+=o}}}var a=w(r,this.clonePosition());return{val:{type:n.literal,value:i,location:a},err:null}},e.prototype.tryParseLeftAngleBracket=function(){return this.isEOF()||60!==this.char()||!this.ignoreTag&&(ie(e=this.peek()||0)||47===e)?null:(this.bump(),"<");var e},e.prototype.tryParseQuote=function(e){if(this.isEOF()||39!==this.char())return null;switch(this.peek()){case 39:return this.bump(),this.bump(),"'";case 123:case 60:case 62:case 125:break;case 35:if("plural"===e||"selectordinal"===e)break;return null;default:return null}this.bump();var t=[this.char()];for(this.bump();!this.isEOF();){var r=this.char();if(39===r){if(39!==this.peek()){this.bump();break}t.push(39),this.bump()}else t.push(r);this.bump()}return Q.apply(void 0,t)},e.prototype.tryParseUnquoted=function(e,t){if(this.isEOF())return null;var r=this.char();return 60===r||123===r||35===r&&("plural"===t||"selectordinal"===t)||125===r&&e>0?null:(this.bump(),Q(r))},e.prototype.parseArgument=function(e,t){var r=this.clonePosition();if(this.bump(),this.bumpSpace(),this.isEOF())return this.error(i.EXPECT_ARGUMENT_CLOSING_BRACE,w(r,this.clonePosition()));if(125===this.char())return this.bump(),this.error(i.EMPTY_ARGUMENT,w(r,this.clonePosition()));var h=this.parseIdentifierIfPossible().value;if(!h)return this.error(i.MALFORMED_ARGUMENT,w(r,this.clonePosition()));if(this.bumpSpace(),this.isEOF())return this.error(i.EXPECT_ARGUMENT_CLOSING_BRACE,w(r,this.clonePosition()));switch(this.char()){case 125:return this.bump(),{val:{type:n.argument,value:h,location:w(r,this.clonePosition())},err:null};case 44:return this.bump(),this.bumpSpace(),this.isEOF()?this.error(i.EXPECT_ARGUMENT_CLOSING_BRACE,w(r,this.clonePosition())):this.parseArgumentOptions(e,t,h,r);default:return this.error(i.MALFORMED_ARGUMENT,w(r,this.clonePosition()))}},e.prototype.parseIdentifierIfPossible=function(){var e=this.clonePosition(),t=this.offset(),r=W(this.message,t),i=t+r.length;return this.bumpTo(i),{value:r,location:w(e,this.clonePosition())}},e.prototype.parseArgumentOptions=function(e,t,r,o){var a,u=this.clonePosition(),l=this.parseIdentifierIfPossible().value,c=this.clonePosition();switch(l){case"":return this.error(i.EXPECT_ARGUMENT_TYPE,w(u,c));case"number":case"date":case"time":this.bumpSpace();var E=null;if(this.bumpIf(",")){this.bumpSpace();var p=this.clonePosition();if((T=this.parseSimpleArgStyleIfPossible()).err)return T;if(0===(_=$(T.val)).length)return this.error(i.EXPECT_ARGUMENT_STYLE,w(this.clonePosition(),this.clonePosition()));E={style:_,styleLocation:w(p,this.clonePosition())}}if((A=this.tryParseArgumentClose(o)).err)return A;var f=w(o,this.clonePosition());if(E&&j(null===E||void 0===E?void 0:E.style,"::",0)){var b=z(E.style.slice(2));if("number"===l)return(T=this.parseNumberSkeletonFromString(b,E.styleLocation)).err?T:{val:{type:n.number,value:r,location:f,style:T.val},err:null};if(0===b.length)return this.error(i.EXPECT_DATE_TIME_SKELETON,f);var g=b;this.locale&&(g=function(e,t){for(var r="",i=0;i<e.length;i++){var n=e.charAt(i);if("j"===n){for(var h=0;i+1<e.length&&e.charAt(i+1)===n;)h++,i++;var s=1+(1&h),o=h<2?1:3+(h>>1),a=O(t);for("H"!=a&&"k"!=a||(o=0);o-- >0;)r+="a";for(;s-- >0;)r=a+r}else r+="J"===n?"H":n}return r}(b,this.locale));var _={type:h.dateTime,pattern:g,location:E.styleLocation,parsedOptions:this.shouldParseSkeletons?S(g):{}};return{val:{type:"date"===l?n.date:n.time,value:r,location:f,style:_},err:null}}return{val:{type:"number"===l?n.number:"date"===l?n.date:n.time,value:r,location:f,style:null!==(a=null===E||void 0===E?void 0:E.style)&&void 0!==a?a:null},err:null};case"plural":case"selectordinal":case"select":var H=this.clonePosition();if(this.bumpSpace(),!this.bumpIf(","))return this.error(i.EXPECT_SELECT_ARGUMENT_OPTIONS,w(H,(0,s.__assign)({},H)));this.bumpSpace();var m=this.parseIdentifierIfPossible(),B=0;if("select"!==l&&"offset"===m.value){if(!this.bumpIf(":"))return this.error(i.EXPECT_PLURAL_ARGUMENT_OFFSET_VALUE,w(this.clonePosition(),this.clonePosition()));var T;if(this.bumpSpace(),(T=this.tryParseDecimalInteger(i.EXPECT_PLURAL_ARGUMENT_OFFSET_VALUE,i.INVALID_PLURAL_ARGUMENT_OFFSET_VALUE)).err)return T;this.bumpSpace(),m=this.parseIdentifierIfPossible(),B=T.val}var A,v=this.tryParsePluralOrSelectOptions(e,l,t,m);if(v.err)return v;if((A=this.tryParseArgumentClose(o)).err)return A;var P=w(o,this.clonePosition());return"select"===l?{val:{type:n.select,value:r,options:q(v.val),location:P},err:null}:{val:{type:n.plural,value:r,options:q(v.val),offset:B,pluralType:"plural"===l?"cardinal":"ordinal",location:P},err:null};default:return this.error(i.INVALID_ARGUMENT_TYPE,w(u,c))}},e.prototype.tryParseArgumentClose=function(e){return this.isEOF()||125!==this.char()?this.error(i.EXPECT_ARGUMENT_CLOSING_BRACE,w(e,this.clonePosition())):(this.bump(),{val:!0,err:null})},e.prototype.parseSimpleArgStyleIfPossible=function(){for(var e=0,t=this.clonePosition();!this.isEOF();){switch(this.char()){case 39:this.bump();var r=this.clonePosition();if(!this.bumpUntil("'"))return this.error(i.UNCLOSED_QUOTE_IN_ARGUMENT_STYLE,w(r,this.clonePosition()));this.bump();break;case 123:e+=1,this.bump();break;case 125:if(!(e>0))return{val:this.message.slice(t.offset,this.offset()),err:null};e-=1;break;default:this.bump()}}return{val:this.message.slice(t.offset,this.offset()),err:null}},e.prototype.parseNumberSkeletonFromString=function(e,t){var r=[];try{r=function(e){if(0===e.length)throw new Error("Number skeleton cannot be empty");for(var t=[],r=0,i=e.split(A).filter((function(e){return e.length>0}));r<i.length;r++){var n=i[r].split("/");if(0===n.length)throw new Error("Invalid number skeleton");for(var h=n[0],s=n.slice(1),o=0,a=s;o<a.length;o++)if(0===a[o].length)throw new Error("Invalid number skeleton");t.push({stem:h,options:s})}return t}(e)}catch(n){return this.error(i.INVALID_NUMBER_SKELETON,t)}return{val:{type:h.number,tokens:r,location:t,parsedOptions:this.shouldParseSkeletons?I(r):{}},err:null}},e.prototype.tryParsePluralOrSelectOptions=function(e,t,r,n){for(var h,s=!1,o=[],a=new Set,u=n.value,l=n.location;;){if(0===u.length){var c=this.clonePosition();if("select"===t||!this.bumpIf("="))break;var E=this.tryParseDecimalInteger(i.EXPECT_PLURAL_ARGUMENT_SELECTOR,i.INVALID_PLURAL_ARGUMENT_SELECTOR);if(E.err)return E;l=w(c,this.clonePosition()),u=this.message.slice(c.offset,this.offset())}if(a.has(u))return this.error("select"===t?i.DUPLICATE_SELECT_ARGUMENT_SELECTOR:i.DUPLICATE_PLURAL_ARGUMENT_SELECTOR,l);"other"===u&&(s=!0),this.bumpSpace();var p=this.clonePosition();if(!this.bumpIf("{"))return this.error("select"===t?i.EXPECT_SELECT_ARGUMENT_SELECTOR_FRAGMENT:i.EXPECT_PLURAL_ARGUMENT_SELECTOR_FRAGMENT,w(this.clonePosition(),this.clonePosition()));var f=this.parseMessage(e+1,t,r);if(f.err)return f;var b=this.tryParseArgumentClose(p);if(b.err)return b;o.push([u,{value:f.val,location:w(p,this.clonePosition())}]),a.add(u),this.bumpSpace(),u=(h=this.parseIdentifierIfPossible()).value,l=h.location}return 0===o.length?this.error("select"===t?i.EXPECT_SELECT_ARGUMENT_SELECTOR:i.EXPECT_PLURAL_ARGUMENT_SELECTOR,w(this.clonePosition(),this.clonePosition())):this.requiresOtherClause&&!s?this.error(i.MISSING_OTHER_CLAUSE,w(this.clonePosition(),this.clonePosition())):{val:o,err:null}},e.prototype.tryParseDecimalInteger=function(e,t){var r=1,i=this.clonePosition();this.bumpIf("+")||this.bumpIf("-")&&(r=-1);for(var n=!1,h=0;!this.isEOF();){var s=this.char();if(!(s>=48&&s<=57))break;n=!0,h=10*h+(s-48),this.bump()}var o=w(i,this.clonePosition());return n?Y(h*=r)?{val:h,err:null}:this.error(t,o):this.error(e,o)},e.prototype.offset=function(){return this.position.offset},e.prototype.isEOF=function(){return this.offset()===this.message.length},e.prototype.clonePosition=function(){return{offset:this.position.offset,line:this.position.line,column:this.position.column}},e.prototype.char=function(){var e=this.position.offset;if(e>=this.message.length)throw Error("out of bound");var t=J(this.message,e);if(void 0===t)throw Error("Offset ".concat(e," is at invalid UTF-16 code unit boundary"));return t},e.prototype.error=function(e,t){return{val:null,err:{kind:e,message:this.message,location:t}}},e.prototype.bump=function(){if(!this.isEOF()){var e=this.char();10===e?(this.position.line+=1,this.position.column=1,this.position.offset+=1):(this.position.column+=1,this.position.offset+=e<65536?1:2)}},e.prototype.bumpIf=function(e){if(j(this.message,e,this.offset())){for(var t=0;t<e.length;t++)this.bump();return!0}return!1},e.prototype.bumpUntil=function(e){var t=this.offset(),r=this.message.indexOf(e,t);return r>=0?(this.bumpTo(r),!0):(this.bumpTo(this.message.length),!1)},e.prototype.bumpTo=function(e){if(this.offset()>e)throw Error("targetOffset ".concat(e," must be greater than or equal to the current offset ").concat(this.offset()));for(e=Math.min(e,this.message.length);;){var t=this.offset();if(t===e)break;if(t>e)throw Error("targetOffset ".concat(e," is at invalid UTF-16 code unit boundary"));if(this.bump(),this.isEOF())break}},e.prototype.bumpSpace=function(){for(;!this.isEOF()&&ne(this.char());)this.bump()},e.prototype.peek=function(){if(this.isEOF())return null;var e=this.char(),t=this.offset(),r=this.message.charCodeAt(t+(e>=65536?2:1));return null!==r&&void 0!==r?r:null},e}();function ie(e){return e>=97&&e<=122||e>=65&&e<=90}function ne(e){return e>=9&&e<=13||32===e||133===e||e>=8206&&e<=8207||8232===e||8233===e}function he(e){return e>=33&&e<=35||36===e||e>=37&&e<=39||40===e||41===e||42===e||43===e||44===e||45===e||e>=46&&e<=47||e>=58&&e<=59||e>=60&&e<=62||e>=63&&e<=64||91===e||92===e||93===e||94===e||96===e||123===e||124===e||125===e||126===e||161===e||e>=162&&e<=165||166===e||167===e||169===e||171===e||172===e||174===e||176===e||177===e||182===e||187===e||191===e||215===e||247===e||e>=8208&&e<=8213||e>=8214&&e<=8215||8216===e||8217===e||8218===e||e>=8219&&e<=8220||8221===e||8222===e||8223===e||e>=8224&&e<=8231||e>=8240&&e<=8248||8249===e||8250===e||e>=8251&&e<=8254||e>=8257&&e<=8259||8260===e||8261===e||8262===e||e>=8263&&e<=8273||8274===e||8275===e||e>=8277&&e<=8286||e>=8592&&e<=8596||e>=8597&&e<=8601||e>=8602&&e<=8603||e>=8604&&e<=8607||8608===e||e>=8609&&e<=8610||8611===e||e>=8612&&e<=8613||8614===e||e>=8615&&e<=8621||8622===e||e>=8623&&e<=8653||e>=8654&&e<=8655||e>=8656&&e<=8657||8658===e||8659===e||8660===e||e>=8661&&e<=8691||e>=8692&&e<=8959||e>=8960&&e<=8967||8968===e||8969===e||8970===e||8971===e||e>=8972&&e<=8991||e>=8992&&e<=8993||e>=8994&&e<=9e3||9001===e||9002===e||e>=9003&&e<=9083||9084===e||e>=9085&&e<=9114||e>=9115&&e<=9139||e>=9140&&e<=9179||e>=9180&&e<=9185||e>=9186&&e<=9254||e>=9255&&e<=9279||e>=9280&&e<=9290||e>=9291&&e<=9311||e>=9472&&e<=9654||9655===e||e>=9656&&e<=9664||9665===e||e>=9666&&e<=9719||e>=9720&&e<=9727||e>=9728&&e<=9838||9839===e||e>=9840&&e<=10087||10088===e||10089===e||10090===e||10091===e||10092===e||10093===e||10094===e||10095===e||10096===e||10097===e||10098===e||10099===e||10100===e||10101===e||e>=10132&&e<=10175||e>=10176&&e<=10180||10181===e||10182===e||e>=10183&&e<=10213||10214===e||10215===e||10216===e||10217===e||10218===e||10219===e||10220===e||10221===e||10222===e||10223===e||e>=10224&&e<=10239||e>=10240&&e<=10495||e>=10496&&e<=10626||10627===e||10628===e||10629===e||10630===e||10631===e||10632===e||10633===e||10634===e||10635===e||10636===e||10637===e||10638===e||10639===e||10640===e||10641===e||10642===e||10643===e||10644===e||10645===e||10646===e||10647===e||10648===e||e>=10649&&e<=10711||10712===e||10713===e||10714===e||10715===e||e>=10716&&e<=10747||10748===e||10749===e||e>=10750&&e<=11007||e>=11008&&e<=11055||e>=11056&&e<=11076||e>=11077&&e<=11078||e>=11079&&e<=11084||e>=11085&&e<=11123||e>=11124&&e<=11125||e>=11126&&e<=11157||11158===e||e>=11159&&e<=11263||e>=11776&&e<=11777||11778===e||11779===e||11780===e||11781===e||e>=11782&&e<=11784||11785===e||11786===e||11787===e||11788===e||11789===e||e>=11790&&e<=11798||11799===e||e>=11800&&e<=11801||11802===e||11803===e||11804===e||11805===e||e>=11806&&e<=11807||11808===e||11809===e||11810===e||11811===e||11812===e||11813===e||11814===e||11815===e||11816===e||11817===e||e>=11818&&e<=11822||11823===e||e>=11824&&e<=11833||e>=11834&&e<=11835||e>=11836&&e<=11839||11840===e||11841===e||11842===e||e>=11843&&e<=11855||e>=11856&&e<=11857||11858===e||e>=11859&&e<=11903||e>=12289&&e<=12291||12296===e||12297===e||12298===e||12299===e||12300===e||12301===e||12302===e||12303===e||12304===e||12305===e||e>=12306&&e<=12307||12308===e||12309===e||12310===e||12311===e||12312===e||12313===e||12314===e||12315===e||12316===e||12317===e||e>=12318&&e<=12319||12320===e||12336===e||64830===e||64831===e||e>=65093&&e<=65094}function se(e){e.forEach((function(e){if(delete e.location,E(e)||p(e))for(var t in e.options)delete e.options[t].location,se(e.options[t].value);else u(e)&&g(e.style)||(l(e)||c(e))&&_(e.style)?delete e.style.location:b(e)&&se(e.children)}))}function oe(e,t){void 0===t&&(t={}),t=(0,s.__assign)({shouldParseSkeletons:!0,requiresOtherClause:!0},t);var r=new re(e,t).parse();if(r.err){var n=SyntaxError(i[r.err.kind]);throw n.location=r.err.location,n.originalMessage=r.err.message,n}return(null===t||void 0===t?void 0:t.captureLocation)||se(r.val),r.val}},26113:function(e,t,r){Object.defineProperty(t,"__esModule",{value:!0}),t.generateENXB=t.generateENXA=t.generateXXHA=t.generateXXAC=t.generateXXLS=void 0;var i=r(21448),n=r(13002);t.generateXXLS=function(e){var t="string"===typeof e?(0,n.parse)(e):e,r=t.pop();return r&&(0,n.isLiteralElement)(r)?(r.value+="SSSSSSSSSSSSSSSSSSSSSSSSS",(0,i.__spreadArray)((0,i.__spreadArray)([],t,!0),[r],!1)):(0,i.__spreadArray)((0,i.__spreadArray)([],t,!0),[{type:n.TYPE.literal,value:"SSSSSSSSSSSSSSSSSSSSSSSSS"}],!1)},t.generateXXAC=function e(t){var r="string"===typeof t?(0,n.parse)(t):t;return r.forEach((function(t){if((0,n.isLiteralElement)(t))t.value=t.value.toUpperCase();else if((0,n.isPluralElement)(t)||(0,n.isSelectElement)(t))for(var r=0,i=Object.values(t.options);r<i.length;r++){e(i[r].value)}else(0,n.isTagElement)(t)&&e(t.children)})),r},t.generateXXHA=function(e){var t="string"===typeof e?(0,n.parse)(e):e,r=t.shift();return r&&(0,n.isLiteralElement)(r)?(r.value="[javascript]"+r.value,(0,i.__spreadArray)([r],t,!0)):(0,i.__spreadArray)([{type:n.TYPE.literal,value:"[javascript]"}],t,!0)};var h="abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ",s="\xe2\u1e03\u0107\u1e0b\xe8\u1e1f\u011d\u1e2b\xed\u0135\u01e9\u013a\u1e41\u0144\u014f\u1e57\u024b\u0155\u015b\u1e6d\u016f\u1e7f\u1e98\u1e8b\u1e8f\u1e93\u1e00\u1e02\u1e08\u1e0a\u1e14\u1e1e\u1e20\u1e22\u1e2c\u0134\u1e34\u013b\u1e3e\u014a\xd5\u1e54\u024a\u0154\u1e60\u1e6e\u0168\u1e7c\u1e84\u1e8c\u0178\u01b5";t.generateENXA=function e(t){var r="string"===typeof t?(0,n.parse)(t):t;return r.forEach((function(t){if((0,n.isLiteralElement)(t))t.value=t.value.split("").map((function(e){var t=h.indexOf(e);return t<0?e:s[t]})).join("");else if((0,n.isPluralElement)(t)||(0,n.isSelectElement)(t))for(var r=0,i=Object.values(t.options);r<i.length;r++){e(i[r].value)}else(0,n.isTagElement)(t)&&e(t.children)})),r},t.generateENXB=function e(t){var r="string"===typeof t?(0,n.parse)(t):t;return r.forEach((function(t){if((0,n.isLiteralElement)(t)){var r=t.value.split("").map((function(e,t){var r=h.indexOf(e);return r<0?e:(t+1)%3===0?s[r].repeat(3):s[r]})).join("");t.value="[!! ".concat(r," !!]")}else if((0,n.isPluralElement)(t)||(0,n.isSelectElement)(t))for(var i=0,o=Object.values(t.options);i<o.length;i++){e(o[i].value)}else(0,n.isTagElement)(t)&&e(t.children)})),r}}}]);
//# sourceMappingURL=113.ade46c2e.chunk.js.map