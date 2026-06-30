int main(){
    int x, y, z, w;

    // pre-conditions
    x = 0;
    assume(y > z);
    w = 0;

    // loop body
    while(unknown()){
        if(x < z){
            w = w + 1;
        }else{
            w = w - 1;
        }
        x = 5 + x;
        y = 3 + y;
        z = 1 + z;
        
    }

    // post-condition
    if(x > y){
        assert(w <= 0);
    }
    
}