! function() {
    if (typeof jQuery === 'undefined') {

        return;
    }
    prettifyCode = function(iframeId) {
        var jsonForm = htmlToJSON(iframeId);

        var prettyCode = '';
        prettyCode += '&lt;' + jsonForm.self.tagName + '&gt;' + prettifyChildren(jsonForm.children, 1) + '<br/>&lt;/' + jsonForm.self.tagName + '&gt;';
        return prettyCode;
    }
    prettifyChildren = function(children, tabLvl) {
        var singletonTags = ['area', 'base', 'br', 'col', 'command', 'embed', 'hr', 'img', 'input', 'link', 'meta', 'param', 'source'];
        var childrenCode = '';
        for (var i = 0; i < children.length; i++) {
            if (children[i].children) {
                var child = '<br/>';
                for (var j = 0; j < tabLvl; j++) {
                    child += '&nbsp;&nbsp;&nbsp;&nbsp;';
                }
                child += '&lt;' + children[i].self.tagName + printAttributes(children[i].self) + '&gt;' + prettifyChildren(children[i].children, tabLvl + 1);
                if (children[i].self.innerContent == '') {
                    for (var j = 0; j < tabLvl + 1; j++) {
                        child += '&nbsp;&nbsp;&nbsp;&nbsp;';
                    }
                    child += children[i].self.innerContent + '<br/>';
                } else {
                    child += '<br/>';
                }
                if (singletonTags.indexOf(children[i].self.tagName) == -1) {
                    for (var j = 0; j < tabLvl; j++) {
                        child += '&nbsp;&nbsp;&nbsp;&nbsp;';
                    }
                    child += '&lt;/' + children[i].self.tagName + '&gt;';
                }
            } else {
                if (children[i].tagName !== 'TEXT_NODE' && children[i].tagName !== 'COMMENT_NODE') {
                    var child = '<br/>';
                    for (var j = 0; j < tabLvl; j++) {
                        child += '&nbsp;&nbsp;&nbsp;&nbsp;';
                    }
                    child += '&lt;' + children[i].tagName + printAttributes(children[i]) + '&gt;';
                    if (children[i].innerContent) {
                        child += '<br/>';
                        for (var j = 0; j < tabLvl + 1; j++) {
                            child += '&nbsp;&nbsp;&nbsp;&nbsp;';
                        }
                        child += children[i].innerContent + '<br/>';
                        for (var j = 0; j < tabLvl; j++) {
                            child += '&nbsp;&nbsp;&nbsp;&nbsp;';
                        }
                    }
                    if (singletonTags.indexOf(children[i].tagName) == -1) {
                        for (var j = 0; j < tabLvl; j++) {
                            child += '&nbsp;&nbsp;&nbsp;&nbsp;';
                        }
                        child += '&lt;/' + children[i].tagName + '&gt;';
                    }
                } else if (children[i].tagName === 'COMMENT_NODE') {
                    var child = '<br/>';
                    for (var j = 0; j < tabLvl; j++) {
                        child += '&nbsp;&nbsp;&nbsp;&nbsp;';
                    }
                    child += '&lt;!--' + children[i].innerContent + '--&gt;';
                } else if (children[i].tagName === 'TEXT_NODE') {
                    var child = '<br/>';
                    for (var j = 0; j < tabLvl; j++) {
                        child += '&nbsp;&nbsp;&nbsp;&nbsp;';
                    }
                    child += children[i].innerContent;
                }
            }

            childrenCode += child;
        }
        return childrenCode;
    }
    printAttributes = function(self) {
        var attributeString = '';
        Object.keys(self).forEach(function(key, index) {
            if (key != 'tagName' && key != 'children' && key != 'innerContent') {
                attributeString += ' ' + key + '="' + self[key] + '"';
            }

        });
        return attributeString;
    }
    htmlToJSON = function(iframeId) {

        constructTagTree = function(tags) {
            if (tags.length != 1 || $(tags[0]).eq(0).contents().length != 0) {
                var newObj = {};

                $.each(tags, function() {
                    var childrenLength = $(this).eq(0).contents().length;
                    var newerObj = [];
                    var count = $(this).eq(0).contents().length;
                    $.each($(this).eq(0).contents(), function() {
                        var child = constructTagTree($(this).eq(0));
                        if (child)
                            newerObj.push(child);
                    });
                    newObj['children'] = (newerObj);
                    newObj['self'] = (constructAttributeObject($(this).eq(0)));

                });
            } else {
                var newObj = {};
                $.each(tags, function() {
                    newObj = (constructAttributeObject($(this).eq(0)));
                });
            }
            return newObj;
        };
        constructAttributeObject = function(element) {
            var attrObj = {};
            element = element[0];
            if ($(element).prop('tagName'))
                attrObj['tagName'] = ($(element).prop('tagName')).toLowerCase();
            else if (element.nodeType == 8) {
                attrObj['tagName'] = 'COMMENT_NODE';
                attrObj['innerContent'] = element.nodeValue;
            } else {
                attrObj['tagName'] = 'TEXT_NODE';
                var x = element.nodeValue;
                x = x.replace(/(\r\n|\n|\r)/gm, " ");
                if (/\S/.test(x)) {
                    attrObj['innerContent'] = x;
                } else {
                    return;
                }
            }
            attrObj['children'] = '';
            if ($(element).prop('tagName'))
                $.each(element.attributes, function() {
                    attrObj[this.name] = this.value;
                });

            return attrObj;
        };
        obj = constructTagTree($(iframeId).contents().eq(0).children().eq(0));
        return obj;
    }
    beautifulSoup = function(url) {
        var _this = this;
        _this.url = url;
        _this.loaded = false;
        _this.content = '';
        _this.onReady = function(action, params) {
            if (_this.loaded === false) {
                $(document.body).append('<iframe id="doc">');
                $('iframe#doc').attr('src', _this.url);
                $('iframe#doc').load(function() {
                    $.get(_this.url, function(data) {
                        _this.loaded = true;
                        _this.content = data;
                        return execute(action, params);
                    });
                });
            } else {
            	console.log(_this.loaded);
                return execute(action, params);
            }
        }
        _this.html2json = function(varToStoreJSON) {
            varToStoreJSON = htmlToJSON('iframe#doc');
        }
        _this.prettify = function(divToPopulate) {
            $(divToPopulate).append($('<textarea />').append(prettifyCode('iframe#doc')).css({width:'80vw',height:'80vh'}));
        }
        execute = function(action, params) {
            if (action === 'html2json') {
                _this.html2json(params);
                return;
            } else if (action === 'prettify') {
                _this.prettify(params);
                return;
            }
        };
    };

}();
