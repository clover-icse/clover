int main(){
    int x, y, z, w;

    // pre-conditions
    x = 0;
    y = 0;
    z = 0;
    w = 0;

    // loop body
    while(unknown()){
        if((y - 10 * x) > 0){
            z = z + 1;
        }else{
            w = w + 1;
        }
        y = y + x;
        x = x + 1;
    }

    // post-condition
    if(x > 100){
        assert(z > w);
    }
    
}