int main(){
    int x, y, w, z;

    // pre-conditions
    x = 0;
    w = 0;
    assume(y > z);

    // loop body
    while(unknown()){
        if(x < z){
            w = w + 1;
        }else{
            w = w - 2;
        }
        x = x + 1;
    }

    // post-condition
    if((x > (y + z))){
        assert((w <= 0));
    }
    
}
