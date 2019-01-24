
//The Base class for our three kinds of Fluxfields
class FluxField{
  constructor(names,flux){
    var ss=FluxField.createSelect(names,flux['source']);
    var exp=document.createElement("INPUT");
    //exp.setAttribute("class",expressionClass);
    exp.value=flux["expression"];
    this.names=names;
    this.select1=ss;
    this.expression=exp;
  }

  //class method  
  static createSelect(names,selected_value) {
    var x = document.createElement("SELECT")
    var i;
    for (i = 0; i < names.length; i++) {
  	  var item=names[i];
      var o = document.createElement("OPTION");
  	  o.value=item;
      var t=document.createTextNode(item);
  	  o.appendChild(t);
  	  x.appendChild(o);
    }
    x.selectedIndex=names.indexOf(selected_value);
    return x;
  }

  //instance setter method  
  set onchange(func){
      this.select1.onchange=func;
      this.expression.onchange=func;
      // call the reporter with the flux as it is at the moment
   
  }

}
class InternalFluxField extends FluxField{
  static update(sf,tf){
    // given two select fields update the possible and selected value
    // of the second field depending on the selected value of the first 
    //
    // it is not necessary to make it a static method of the class 
    // but just more readable
    var si=sf.selectedIndex;
    var tos=tf.options;
    var l=tos.length;

    //clean up old disablements
    for (var i = 0; i < l; i++) {
      tos[i].disabled=false;
    }
    //disable the source pool
    tos[si].disabled=true;
    //if the target pool was set to the new value of the source pool
    //change it
    if (tf.selectedIndex==si){
      tf.selectedIndex=(si+1)%l;
    }
  }
  static update_maker(sf,tf,callback){
    // create a closure that can be mapped to 
    // the "oninput" of the first form
    //
    // question mm 9-20-1018:
    // I  looks as if we could do without this function that
    // just binds the update to the two connected select fields,
    // but I was not able to bind the update function succesfully 
    // if it was just operating on the instance
    // I guess that this is a consequence of lazy evaluation 
    // and the crucial ingrediant is the protection of the 
    // local scope of this function. 
    //
    // it is not necessary to make it a static method of the class 
    // but just more readable
  	var f=function() {
  		InternalFluxField.update(sf,tf);
      callback();
  	};
  	return f;
  };
  constructor(names,flux) {
    // before we can use 'this' we have to call the constructor of the
    // superclass
    super(names,flux);
    var ts=FluxField.createSelect(names,flux['target']);
    var emptyCallBack=function(){ };
    this.select1.oninput=InternalFluxField.update_maker(this.select1,ts,emptyCallBack);
    this.select2=ts;
    
  }
  get value(){
    var val={
      'source':this.select1.value,
      'target':this.select2.value,
      'expression':this.expression.value
    }
    return val;
  }
  //instance setter method  
  set onchange(func){
   
    this.select1.onchange=InternalFluxField.update_maker(this.select1,this.select2,func);
    this.select2.onchange=func;
    this.expression.onchange=func;
  }

}
