/* 
 * @author: timon w. mesulam
 * @email: timon.w.mesulam935xpacenuchra@gmail.com
 * @date: Fri Feb 12 01:05:43 EAT 2021
 * @version: 1.0a-00.1
 * @licence:
 * @description: Simple script addressing source code preview tabs failure in 
 *     android developers offline documentation download from https://androidsdkoffline.blogspot.com/p/android-offline-documentation-download.html since some sourced
 *     files(notably *.js) in *.html files are missing.
 *
 */
var devsite_selectors = document.querySelectorAll("devsite-selector");
for (var i=0, il=devsite_selectors.length; i < il; i++){

    var tabs = devsite_selectors[i].querySelectorAll("[class=devsite-tabs-wrapper]>tab[role=tab]");

    for (var j=0, jl=tabs.length; j < jl; j++){
	tabs[j].addEventListener("click",
	    function (i){
		return function (e){burst.call(this, e, i)}
	    }(devsite_selectors[i]));
    }
}

function burst(e, devsite_selector){
    e.preventDefault();

    var active_tab = devsite_selector.getAttribute("active"),
	tab_name = this.getAttribute("tab");

    if (tab_name === active_tab)
	return;

    var prev_tab = devsite_selector.querySelectorAll("tab[id="+ active_tab +"]")[0],
	tab_section = devsite_selector.querySelectorAll("section[tab="+ tab_name +"]")[0],
	prev_tab_section = devsite_selector.querySelectorAll("section[tab="+ active_tab +"]")[0];

    devsite_selector.setAttribute("active", tab_name);

    prev_tab.setAttribute("aria-selected", "false");
    this.setAttribute("aria-selected","true");

    prev_tab.removeAttribute("active");
    this.setAttribute("active", "");

    prev_tab_section.removeAttribute("active");
    tab_section.setAttribute("active", "");

    prev_tab_section.style.visibility = "hidden";
    tab_section.style.visibility = "visible";
}
