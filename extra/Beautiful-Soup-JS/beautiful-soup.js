//Beautiful Soup JS
//Inspired by Beautiful Soup, served with love in JS
//Author: maligndrome
!function(){
	if (typeof jQuery === 'undefined') {
  console.log("Beautiful Soup requires JQuery.");
  return;
}
prettifyCode = function (iframeId) {
	var jsonForm=htmlToJSON(iframeId);
	console.log(jsonForm);
	var prettyCode='';
	prettyCode+='&lt;'+jsonForm.self.tagName+'&gt;'+prettifyChildren(jsonForm.children,1)+'<br/>&lt;/'+jsonForm.self.tagName+'&gt;';
	return prettyCode;
}
prettifyChildren = function(children,tabLvl) {
	var childrenCode='';
	for(var i=0;i<children.length;i++) {
		if(children[i].children){
			var child='<br/>';
			for(var j=0;j<tabLvl;j++){
				child+='&nbsp;&nbsp;&nbsp;&nbsp;';
			}
			child+='&lt;'+children[i].self.tagName+printAttributes(children[i].self)+'&gt;'+prettifyChildren(children[i].children,tabLvl+1);
			if(children[i].self.innerContent==''){
				for(var j=0;j<tabLvl+1;j++){
					child+='&nbsp;&nbsp;&nbsp;&nbsp;';
				}
				child+=children[i].self.innerContent+'<br/>';
			}
			for(var j=0;j<tabLvl;j++){
				child+='&nbsp;&nbsp;&nbsp;&nbsp;';
			}
			child+='&lt;/'+children[i].self.tagName+'&gt;';
		}
		else
		{
			if(children[i].tagName!=='TEXT_NODE'&&children[i].tagName!=='COMMENT_NODE'){
				var child='<br/>';
				for(var j=0;j<tabLvl;j++){
					child+='&nbsp;&nbsp;&nbsp;&nbsp;';
				}
				child+='&lt;'+children[i].tagName+printAttributes(children[i])+'&gt;<br/>';
				for(var j=0;j<tabLvl+1;j++){
					child+='&nbsp;&nbsp;&nbsp;&nbsp;';
				}
				child+=children[i].innerContent+'<br/>';
				for(var j=0;j<tabLvl;j++){
					child+='&nbsp;&nbsp;&nbsp;&nbsp;';
				}
				child+='&lt;/'+children[i].tagName+'&gt;';
			}
			else if(children[i].tagName==='COMMENT_NODE'){
				var child='<br/>';
				for(var j=0;j<tabLvl;j++){
					child+='&nbsp;&nbsp;&nbsp;&nbsp;';
				}
				child+='&lt;!--'+children[i].innerContent+'--&gt;';
			} else if(children[i].innerContent!==''){
				var child='<br/>';
				for(var j=0;j<tabLvl;j++){
					child+='&nbsp;&nbsp;&nbsp;&nbsp;';
				}
				child+=children[i].innerContent;
			}
		}
		
		childrenCode+=child;
	}
	return childrenCode;
}
printAttributes=function(self){
	var attributeString='';
	Object.keys(self).forEach(function(key,index) {
		if(key!='tagName'&&key!='children'&&key!='innerContent'){
			attributeString+=' '+key+'="'+self[key]+'"';
		}
	    
	});
	return attributeString;
}
htmlToJSON = function(iframeId) {
	//helper function!
	constructTagTree= function(tags){
		if(tags.length!=1 || $(tags[0]).eq(0).contents().length!=0){
			var newObj={};
			console.log("tags fed in are:", tags);
			$.each(tags, function(){
				var childrenLength=$(this).eq(0).contents().length;
				// console.log($(this).eq(0),childrenLength);
				// if(childrenLength==0){
				// 	console.log('childless object:',$(this).eq(0));
				// 	newObj['self']=(constructAttributeObject($(this).eq(0)));
				// 	newObj['children']='';
				// }
				// else {
					var newerObj=[];
					var count=$(this).eq(0).contents().length;
					$.each($(this).eq(0).contents(),function(){
						newerObj.push(constructTagTree($(this).eq(0)));				
					});		
					newObj['children']=(newerObj);	
					newObj['self']=	 (constructAttributeObject($(this).eq(0)));
				//}
			});
		} else {
			var newObj={};
			$.each(tags, function(){
					newObj=(constructAttributeObject($(this).eq(0)));
					// var remainingContent=$(this)
					// 		        .clone()    
					// 		        .children() 
					// 		        .remove()   
					// 		        .end()  
					// 		        .text();
					// 		remainingContent=remainingContent.replace(/(\r\n|\n|\r)/gm, " ");
					// 		if (/\S/.test(remainingContent)) {
					// 		   newObj['innerContent']=remainingContent;   
					// 		}
					
			});
		}
		return newObj;
	};
	constructAttributeObject = function(element) {
		var attrObj={};
		element=element[0];
		if($(element).prop('tagName'))
		attrObj['tagName']=($(element).prop('tagName')).toLowerCase();
		else if(element.nodeType==8){
			attrObj['tagName']='COMMENT_NODE';
			attrObj['innerContent']=element.nodeValue;
		}else{
			attrObj['tagName']='TEXT_NODE';
			var x=element.nodeValue;
			x=x.replace(/(\r\n|\n|\r)/gm, " ");
			if (/\S/.test(x)) {
			    attrObj['innerContent']=x;   
			} else {
				attrObj['innerContent']='';
			}
		}
		// var remainingContent=$(this).parent()
		// 					        .clone()    
		// 					        .children() 
		// 					        .remove()   
		// 					        .end()  
		// 					        .text();
		// remainingContent=remainingContent.replace(/(\r\n|\n|\r)/gm, " ");
		// if (/\S/.test(remainingContent)) {
		//     attrObj['innerContent']=remainingContent;   
		// } else {
		// 	attrObj['innerContent']='';
		// }
		attrObj['children']='';
		if($(element).prop('tagName'))
		$.each(element.attributes, function(){
			attrObj[this.name]=this.value;
		});
		console.log(attrObj);
		return attrObj;
	};
	obj = constructTagTree($(iframeId).contents().eq(0).children().eq(0));
	return obj;
}
beautifulSoup = function(url){
	var _this=this;
	this.url=url;
	this.loaded=false;
	this.content='';
	this.onReady = function(action,params){
		console.log(action);
		if(this.loaded===false){
			$(document.body).append('<iframe id="doc">');
		    $('iframe#doc').attr('src', _this.url);

		    $('iframe#doc').load(function() {
		        $.get(_this.url, function(data) {
				   _this.loaded=true;
				   _this.content=data;
				   execute(action,params);
				   return;
				});
		    });
			
		}
		else {
			execute(action);
			return;
		}
	}
	_this.writeToConsole = function(){
		//if(this.loaded)
		//console.log(_this.content);
		htmlToJSON('iframe#doc');
		//else
	}
	_this.prettify = function(divToPopulate){
		//console.log();
		$(divToPopulate).append($('<pre></pre>').append(prettifyCode('iframe#doc')));
	}
	execute= function(action,params){
		console.log('executing...');
		if(action==='writeToConsole'){
			_this.writeToConsole();
		} else if(action==='prettify'){
			_this.prettify(params);
		}
	};
};

}();