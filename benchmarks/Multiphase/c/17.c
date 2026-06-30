int main(){
    int x, z, v, w;

    // pre-conditions
    assume(x > z);
    v = 0;
    w = 0;

    // loop body
    while(unknown()){
        if(x < z){
            v = v + 1;
        }else{
            w = w + 1;
        }
        x = x + 1;
        z = z + 2;
        
    }

    // post-condition
    if(v > 1000){
        assert(w > 0);
    }
    
}